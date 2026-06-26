import json
import logging
import time
import os
import hashlib
from neo4j import GraphDatabase
from tqdm import tqdm

def generate_hash(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def normalize_class_name(name):
    if not name: return name
    name = name.split('<')[0]
    if '::' in name:
        name = name.split('::')[-1]
    name = name.replace('class ', '').replace('struct ', '').strip()
    return name

def normalize_parameter_type(type_str):
    if not type_str: return ""
    t = type_str
    t = t.replace('const ', '').replace(' const', '')
    t = t.replace('class ', '').replace('struct ', '').replace('typename ', '')
    t = t.replace('*', '').replace('&', '')
    t = t.strip()
    return t

def normalize_return_type(type_str):
    # Base stripping
    base = type_str.replace('const', '').replace('*', '').replace('&', '').strip()
    
    # Strip some common noise (if not already done by parser)
    noise_keywords = ['virtual', 'inline', 'static', 'explicit', 'friend']
    for k in noise_keywords:
        if base.startswith(k + ' '):
            base = base[len(k)+1:].strip()
            
    # Handle templates roughly by dropping <...> if we just want base class
    # For return types, sometimes knowing it's a vector is enough, but to match classes:
    template_idx = base.find('<')
    if template_idx != -1:
        base = base[:template_idx].strip()
        
    return base

import re

def clean_documentation(doc_text):
    if not doc_text:
        return ""
    # Remove basic HTML tags safely (avoiding <T> templates)
    # Tags like <p>, <br>, <div>, etc.
    doc_text = re.sub(r'</?(p|br|div|span|b|i|strong|em|ul|li|ol)[^>]*>', ' ', doc_text, flags=re.IGNORECASE)
    # Normalize multiple newlines
    doc_text = re.sub(r'\n{3,}', '\n\n', doc_text)
    # Normalize multiple spaces
    doc_text = re.sub(r'[ \t]+', ' ', doc_text)
    return doc_text.strip()

PRIMITIVE_TYPES = {'int', 'double', 'float', 'bool', 'char', 'void', 'size_t', 'long', 'short', 'unsigned', 'signed'}

# Configure logging
logging.basicConfig(
    filename='graph_build.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class KnowledgeGraphBuilder:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            self.driver.verify_connectivity()
            logging.info("Successfully connected to Neo4j.")
            print("Successfully connected to Neo4j.")
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            print(f"Failed to connect to Neo4j: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def reset_database(self):
        if not self.driver:
            return False
        try:
            with self.driver.session() as session:
                # Delete all nodes and edges
                session.run("MATCH (n) DETACH DELETE n")
                logging.info("Deleted existing nodes and edges.")
                
                # Drop existing constraints
                constraints = session.run("SHOW CONSTRAINTS YIELD name, labelsOrTypes, properties").data()
                for c in constraints:
                    session.run(f"DROP CONSTRAINT {c['name']}")
                    logging.info(f"Dropped old constraint: {c['name']}")
                        
                return True
        except Exception as e:
            logging.error(f"Failed to reset database: {e}")
            return False

    def create_constraints(self):
        if not self.driver:
            return False
        try:
            with self.driver.session() as session:
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (f:File) REQUIRE f.path IS UNIQUE")
                session.run("CREATE CONSTRAINT class_id_unique IF NOT EXISTS FOR (c:Class) REQUIRE c.id IS UNIQUE")
                session.run("CREATE CONSTRAINT external_class_id_unique IF NOT EXISTS FOR (e:ExternalClass) REQUIRE e.id IS UNIQUE")
                session.run("CREATE CONSTRAINT function_id_unique IF NOT EXISTS FOR (fn:Function) REQUIRE fn.id IS UNIQUE")
                session.run("CREATE CONSTRAINT function_fqn_unique IF NOT EXISTS FOR (fn:Function) REQUIRE fn.fqn IS UNIQUE")
                session.run("CREATE CONSTRAINT method_id_unique IF NOT EXISTS FOR (m:Method) REQUIRE m.id IS UNIQUE")
                session.run("CREATE CONSTRAINT method_fqn_unique IF NOT EXISTS FOR (m:Method) REQUIRE m.fqn IS UNIQUE")
                session.run("CREATE CONSTRAINT parameter_id_unique IF NOT EXISTS FOR (p:Parameter) REQUIRE p.id IS UNIQUE")
                session.run("CREATE CONSTRAINT primitive_type_name_unique IF NOT EXISTS FOR (p:PrimitiveType) REQUIRE p.name IS UNIQUE")
                session.run("CREATE CONSTRAINT external_type_name_unique IF NOT EXISTS FOR (e:ExternalType) REQUIRE e.name IS UNIQUE")
                session.run("CREATE CONSTRAINT enum_id_unique IF NOT EXISTS FOR (e:Enum) REQUIRE e.id IS UNIQUE")
                session.run("CREATE CONSTRAINT enumvalue_id_unique IF NOT EXISTS FOR (ev:EnumValue) REQUIRE ev.id IS UNIQUE")
                session.run("CREATE CONSTRAINT struct_id_unique IF NOT EXISTS FOR (s:Struct) REQUIRE s.id IS UNIQUE")
                session.run("CREATE CONSTRAINT typedef_id_unique IF NOT EXISTS FOR (t:Typedef) REQUIRE t.id IS UNIQUE")
                session.run("CREATE CONSTRAINT doc_id_unique IF NOT EXISTS FOR (d:Documentation) REQUIRE d.id IS UNIQUE")
                session.run("CREATE CONSTRAINT build_config_name_unique IF NOT EXISTS FOR (b:BuildConfiguration) REQUIRE b.name IS UNIQUE")
            logging.info("Constraints verified/created.")
            return True
        except Exception as e:
            logging.error(f"Failed to create constraints: {e}")
            return False

    def load_data(self, json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logging.info(f"Loaded {len(data)} file records from {json_path}")
            return data
        except Exception as e:
            logging.error(f"Failed to load JSON data: {e}")
            return None

    def build_graph(self, data):
        if not self.driver:
            return {}
            
        stats = {
            'files_loaded': 0,
            'classes_loaded': 0,
            'inheritance_loaded': 0,
            'functions_loaded': 0,
            'methods_loaded': 0,
            'parameters_loaded': 0,
            'uses_type_loaded': 0,
            'returns_loaded': 0,
            'primitive_nodes_created': 0,
            'external_nodes_created': 0,
            'enums_loaded': 0,
            'enum_values_loaded': 0,
            'structs_loaded': 0,
            'typedefs_loaded': 0,
            'aliases_loaded': 0,
            'docs_loaded': 0,
            'failures': 0,
            'start_time': time.time()
        }
        
        # 1. Build dictionary for Option A (Lookup Strategy)
        name_to_id = {}
        for item in data:
            path = item.get('path')
            if not path: continue
            for cls in item.get('classes', []):
                name = cls.get('name')
                fqn = cls.get('fqn')
                if name:
                    class_id = fqn if fqn else f"{path}::{name}"
                    name_to_id[class_id] = class_id
                    norm_name = normalize_class_name(name)
                    if norm_name not in name_to_id:
                        name_to_id[norm_name] = class_id
                        
        # Collect all defined class/struct FQNs to distinguish internal vs external methods
        defined_types = set()
        for item in data:
            path = item.get('path')
            if not path: continue
            for cls in item.get('classes', []):
                name = cls.get('name')
                fqn = cls.get('fqn')
                if name:
                    class_id = fqn if fqn else f"{path}::{name}"
                    defined_types.add(class_id)
            for s in item.get('structs', []):
                name = s.get('name')
                fqn = s.get('fqn')
                if name:
                    struct_id = fqn if fqn else generate_hash(f"{path}::struct::{name}::{s.get('line_number', 0)}")
                    defined_types.add(struct_id)

        # Prepare batches
        file_batch = []
        class_batch = []
        internal_inheritance_batch = []
        external_inheritance_batch = []
        function_batch = []
        internal_method_batch = []
        external_method_batch = []
        parameter_batch = []
        uses_type_batch = []
        primitive_type_batch = []
        external_type_batch = []
        returns_batch = []
        
        enum_batch = []
        enum_value_batch = []
        struct_batch = []
        typedef_batch = []
        aliases_batch = []
        
        doc_batch = []
        
        build_config_batch = []
        compiled_with_batch = []
        active_in_config_batch = []
        includes_batch = []
        
        for item in data:
            try:
                path = item.get('path')
                if not path: continue
                
                if 'file' in item:
                    file_batch.append({
                        'path': path,
                        'file': item['file']
                    })

                build_configuration = item.get('build_configuration')
                if build_configuration:
                    config_name = build_configuration.get('name', 'Default')
                    compiler = build_configuration.get('compiler', 'unknown')
                    standard = build_configuration.get('standard', 'unknown')
                    flags = build_configuration.get('flags', [])
                    
                    if not any(b['name'] == config_name for b in build_config_batch):
                        build_config_batch.append({
                            'name': config_name,
                            'compiler': compiler,
                            'standard': standard,
                            'flags': flags
                        })
                    
                    compiled_with_batch.append({
                        'file_path': path,
                        'config_name': config_name
                    })

                for inc in item.get('includes', []):
                    includes_batch.append({
                        'from_path': path,
                        'to_path': inc
                    })
                
                # Enums
                for e in item.get('enums', []):
                    name = e.get('name')
                    fqn = e.get('fqn')
                    if name:
                        ln = e.get('line_number', 0)
                        enum_id = fqn if fqn else generate_hash(f"{path}::enum::{name}::{ln}")
                        enum_batch.append({
                            'id': enum_id,
                            'name': name,
                            'fqn': enum_id,
                            'documentation': e.get('documentation', ''),
                            'line_number': ln,
                            'file_path': path
                        })
                        if build_configuration:
                            active_in_config_batch.append({
                                'entity_id': enum_id,
                                'entity_type': 'Enum',
                                'config_name': config_name
                            })
                        
                        doc = clean_documentation(e.get('documentation', ''))
                        if doc:
                            doc_id = generate_hash(f"{enum_id}::doc")
                            doc_batch.append({
                                'id': doc_id,
                                'text': doc,
                                'length': len(doc),
                                'entity_type': 'Enum',
                                'entity_name': name,
                                'file_path': path,
                                'parent_id': enum_id,
                                'parent_label': 'Enum'
                            })
                            
                        for pos, v in enumerate(e.get('values', [])):
                            ev_id = generate_hash(f"{enum_id}::value::{v}::{pos}")
                            enum_value_batch.append({
                                'id': ev_id,
                                'parent_id': enum_id,
                                'name': v,
                                'value': v,
                                'position': pos
                            })

                # Structs
                for s in item.get('structs', []):
                    name = s.get('name')
                    fqn = s.get('fqn')
                    if name:
                        ln = s.get('line_number', 0)
                        struct_id = fqn if fqn else generate_hash(f"{path}::struct::{name}::{ln}")
                        struct_batch.append({
                            'id': struct_id,
                            'name': name,
                            'fqn': struct_id,
                            'documentation': s.get('documentation', ''),
                            'line_number': ln,
                            'file_path': path
                        })
                        if build_configuration:
                            active_in_config_batch.append({
                                'entity_id': struct_id,
                                'entity_type': 'Struct',
                                'config_name': config_name
                            })
                        
                        doc = clean_documentation(s.get('documentation', ''))
                        if doc:
                            doc_id = generate_hash(f"{struct_id}::doc")
                            doc_batch.append({
                                'id': doc_id,
                                'text': doc,
                                'length': len(doc),
                                'entity_type': 'Struct',
                                'entity_name': name,
                                'file_path': path,
                                'parent_id': struct_id,
                                'parent_label': 'Struct'
                            })

                # Typedefs
                for t in item.get('typedefs', []):
                    name = t.get('name')
                    fqn = t.get('fqn')
                    if name:
                        ln = t.get('line_number', 0)
                        typedef_id = fqn if fqn else generate_hash(f"{path}::typedef::{name}::{ln}")
                        typedef_batch.append({
                            'id': typedef_id,
                            'name': name,
                            'fqn': typedef_id,
                            'target_type': "", # JSON doesn't contain target type
                            'documentation': t.get('documentation', ''),
                            'line_number': ln,
                            'file_path': path
                        })
                        if build_configuration:
                            active_in_config_batch.append({
                                'entity_id': typedef_id,
                                'entity_type': 'Typedef',
                                'config_name': config_name
                            })
                
                # Classes
                for cls in item.get('classes', []):
                    name = cls.get('name')
                    fqn = cls.get('fqn')
                    if name:
                        class_id = fqn if fqn else f"{path}::{name}"
                        class_batch.append({
                            'id': class_id,
                            'fqn': class_id,
                            'path': path,
                            'name': name,
                            'documentation': cls.get('documentation', ''),
                            'line_number': cls.get('line_number', 0)
                        })
                        if build_configuration:
                            active_in_config_batch.append({
                                'entity_id': class_id,
                                'entity_type': 'Class',
                                'config_name': config_name
                            })
                        
                        doc = clean_documentation(cls.get('documentation', ''))
                        if doc:
                            doc_id = generate_hash(f"{class_id}::doc")
                            doc_batch.append({
                                'id': doc_id,
                                'text': doc,
                                'length': len(doc),
                                'entity_type': 'Class',
                                'entity_name': name,
                                'file_path': path,
                                'parent_id': class_id,
                                'parent_label': 'Class'
                            })
                
                # Inheritance
                for inh in item.get('inheritance', []):
                    child_fqn = inh.get('class_fqn')
                    base_fqn = inh.get('base_fqn')
                    child_name = inh.get('class')
                    base_name = inh.get('base')
                    
                    if child_fqn and base_fqn:
                        if not base_fqn.startswith("unresolved::"):
                            internal_inheritance_batch.append({
                                'child_id': child_fqn,
                                'base_id': base_fqn
                            })
                        else:
                            clean_base = base_fqn.replace("unresolved::", "")
                            external_inheritance_batch.append({
                                'child_id': child_fqn,
                                'base_id': base_fqn,
                                'base_name': clean_base
                            })
                            
                # Functions
                for fn in item.get('functions', []):
                    name = fn.get('name')
                    fqn = fn.get('fqn')
                    if name:
                        params = fn.get('parameters', [])
                        param_str = ", ".join(p.get('type', '') for p in params)
                        signature = f"{name}({param_str})"
                        line_number = fn.get('line_number', 0)
                        ret_type = fn.get('return_type', '')
                        ret_type_fqn = fn.get('return_type_fqn', '')
                        
                        func_fqn = fqn if fqn else name
                        raw_id = f"{path}::{func_fqn}::{signature}::{line_number}"
                        func_id = generate_hash(raw_id)
                        
                        function_batch.append({
                            'id': func_id,
                            'fqn': func_fqn,
                            'path': path,
                            'name': name,
                            'signature': signature,
                            'return_type': ret_type,
                            'documentation': fn.get('documentation', ''),
                            'line_number': line_number
                        })
                        if build_configuration:
                            active_in_config_batch.append({
                                'entity_id': func_id,
                                'entity_type': 'Function',
                                'config_name': config_name
                            })
                        
                        doc = clean_documentation(fn.get('documentation', ''))
                        if doc:
                            doc_id = generate_hash(f"{func_id}::doc")
                            doc_batch.append({
                                'id': doc_id,
                                'text': doc,
                                'length': len(doc),
                                'entity_type': 'Function',
                                'entity_name': name,
                                'file_path': path,
                                'parent_id': func_id,
                                'parent_label': 'Function'
                            })
                        
                        for pos, p in enumerate(params):
                            p_name = p.get('name', '')
                            p_type = p.get('type', '')
                            p_type_fqn = p.get('type_fqn', '')
                            raw_p_id = f"{func_id}::param::{pos}::{p_name}::{p_type}"
                            p_id = generate_hash(raw_p_id)
                            
                            parameter_batch.append({
                                'id': p_id,
                                'parent_id': func_id,
                                'parent_type': 'Function',
                                'name': p_name,
                                'type': p_type,
                                'position': pos,
                                'default_value': p.get('default_value', None),
                                'is_const': 'const ' in p_type or ' const' in p_type,
                                'is_pointer': '*' in p_type,
                                'is_reference': '&' in p_type
                            })
                            
                            if p_type_fqn and not p_type_fqn.startswith("unresolved::"):
                                uses_type_batch.append({
                                    'param_id': p_id,
                                    'class_id': p_type_fqn
                                })
                                
                        if not ret_type:
                            ret_type = 'void'
                            ret_type_fqn = 'void'
                            
                        if ret_type_fqn:
                            if ret_type_fqn in PRIMITIVE_TYPES:
                                primitive_type_batch.append({'name': ret_type_fqn})
                                returns_batch.append({'parent_id': func_id, 'target_type': 'PrimitiveType', 'name': ret_type_fqn})
                            elif not ret_type_fqn.startswith("unresolved::"):
                                returns_batch.append({'parent_id': func_id, 'target_type': 'Class', 'id': ret_type_fqn})
                            else:
                                clean_ret = ret_type_fqn.replace("unresolved::", "")
                                external_type_batch.append({'name': clean_ret})
                                returns_batch.append({'parent_id': func_id, 'target_type': 'ExternalType', 'name': clean_ret})

                # Methods
                for md in item.get('methods', []):
                    name = md.get('name')
                    class_name = md.get('class')
                    class_fqn = md.get('class_fqn')
                    fqn = md.get('fqn')
                    if name and (class_fqn or class_name):
                        params = md.get('parameters', [])
                        param_str = ", ".join(p.get('type', '') for p in params)
                        signature = f"{name}({param_str})"
                        line_number = md.get('line_number', 0)
                        ret_type = md.get('return_type', '')
                        ret_type_fqn = md.get('return_type_fqn', '')
                        
                        method_fqn = fqn if fqn else f"{class_name}::{name}"
                        raw_id = f"{path}::{method_fqn}::{signature}::{line_number}"
                        method_id = generate_hash(raw_id)
                        
                        if class_fqn and class_fqn in defined_types:
                            internal_method_batch.append({
                                'id': method_id,
                                'fqn': method_fqn,
                                'path': path,
                                'class_id': class_fqn,
                                'name': name,
                                'signature': signature,
                                'return_type': ret_type,
                                'documentation': md.get('documentation', ''),
                                'line_number': line_number
                            })
                        else:
                            external_method_batch.append({
                                'id': method_id,
                                'fqn': method_fqn,
                                'path': path,
                                'class_name': class_fqn if class_fqn else class_name,
                                'name': name,
                                'signature': signature,
                                'return_type': ret_type,
                                'documentation': md.get('documentation', ''),
                                'line_number': line_number
                            })
                        if build_configuration:
                            active_in_config_batch.append({
                                'entity_id': method_id,
                                'entity_type': 'Method',
                                'config_name': config_name
                            })
                            
                        doc = clean_documentation(md.get('documentation', ''))
                        if doc:
                            doc_id = generate_hash(f"{method_id}::doc")
                            doc_batch.append({
                                'id': doc_id,
                                'text': doc,
                                'length': len(doc),
                                'entity_type': 'Method',
                                'entity_name': name,
                                'file_path': path,
                                'parent_id': method_id,
                                'parent_label': 'Method'
                            })
                            
                        for pos, p in enumerate(params):
                            p_name = p.get('name', '')
                            p_type = p.get('type', '')
                            p_type_fqn = p.get('type_fqn', '')
                            raw_p_id = f"{method_id}::param::{pos}::{p_name}::{p_type}"
                            p_id = generate_hash(raw_p_id)
                            
                            parameter_batch.append({
                                'id': p_id,
                                'parent_id': method_id,
                                'parent_type': 'Method',
                                'name': p_name,
                                'type': p_type,
                                'position': pos,
                                'default_value': p.get('default_value', None),
                                'is_const': 'const ' in p_type or ' const' in p_type,
                                'is_pointer': '*' in p_type,
                                'is_reference': '&' in p_type
                            })
                            
                            if p_type_fqn and not p_type_fqn.startswith("unresolved::"):
                                uses_type_batch.append({
                                    'param_id': p_id,
                                    'class_id': p_type_fqn
                                })
                                
                        if not ret_type:
                            ret_type = 'void'
                            ret_type_fqn = 'void'
                            
                        if ret_type_fqn:
                            if ret_type_fqn in PRIMITIVE_TYPES:
                                primitive_type_batch.append({'name': ret_type_fqn})
                                returns_batch.append({'parent_id': method_id, 'target_type': 'PrimitiveType', 'name': ret_type_fqn})
                            elif not ret_type_fqn.startswith("unresolved::"):
                                returns_batch.append({'parent_id': method_id, 'target_type': 'Class', 'id': ret_type_fqn})
                            else:
                                clean_ret = ret_type_fqn.replace("unresolved::", "")
                                external_type_batch.append({'name': clean_ret})
                                returns_batch.append({'parent_id': method_id, 'target_type': 'ExternalType', 'name': clean_ret})
                        
            except Exception as e:
                logging.error(f"Error parsing record: {e}")
                stats['failures'] += 1
                
        batch_size = 500
        
        # Load Files
        def load_files_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (f:File {path: row.path})
            SET f.file = row.file
            """
            tx.run(query, batch=batch)
            
        logging.info("Starting file nodes load...")
        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(file_batch), batch_size), desc="Files"):
                    batch = file_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_files_tx, batch)
                        stats['files_loaded'] += len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load file batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error during file processing: {e}")

        # Load BuildConfigurations
        def load_build_configs_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (b:BuildConfiguration {name: row.name})
            SET b.compiler = row.compiler, b.standard = row.standard, b.flags = row.flags
            """
            tx.run(query, batch=batch)

        if build_config_batch:
            logging.info("Starting BuildConfiguration nodes load...")
            try:
                with self.driver.session() as session:
                    session.execute_write(load_build_configs_tx, build_config_batch)
            except Exception as e:
                logging.error(f"Error during BuildConfiguration processing: {e}")
                stats['failures'] += 1

        # Load COMPILED_WITH
        def load_compiled_with_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (f:File {path: row.file_path})
            MATCH (b:BuildConfiguration {name: row.config_name})
            MERGE (f)-[:COMPILED_WITH]->(b)
            """
            tx.run(query, batch=batch)

        if compiled_with_batch:
            logging.info("Starting COMPILED_WITH relationships load...")
            try:
                with self.driver.session() as session:
                    for i in range(0, len(compiled_with_batch), batch_size):
                        batch = compiled_with_batch[i:i+batch_size]
                        session.execute_write(load_compiled_with_tx, batch)
            except Exception as e:
                logging.error(f"Error during COMPILED_WITH processing: {e}")
                stats['failures'] += 1

        # Load File Includes
        def load_includes_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (f1:File {path: row.from_path})
            MERGE (f2:File {path: row.to_path})
            MERGE (f1)-[:INCLUDES]->(f2)
            """
            tx.run(query, batch=batch)

        if includes_batch:
            logging.info("Starting INCLUDES relationships load...")
            try:
                with self.driver.session() as session:
                    for i in range(0, len(includes_batch), batch_size):
                        batch = includes_batch[i:i+batch_size]
                        session.execute_write(load_includes_tx, batch)
            except Exception as e:
                logging.error(f"Error during INCLUDES processing: {e}")
                stats['failures'] += 1

        # Load Classes
        def load_classes_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (c:Class {id: row.id})
            SET c.name = row.name, c.fqn = row.fqn, c.documentation = row.documentation, c.line_number = row.line_number
            WITH c, row
            MATCH (f:File {path: row.path})
            MERGE (f)-[:CONTAINS]->(c)
            """
            tx.run(query, batch=batch)
            
        logging.info("Starting class nodes load...")
        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(class_batch), batch_size), desc="Classes"):
                    batch = class_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_classes_tx, batch)
                        stats['classes_loaded'] += len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load class batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error during class processing: {e}")
            
        # Load Internal Inheritance
        def load_internal_inheritance_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (c1:Class {id: row.child_id})
            MATCH (c2:Class {id: row.base_id})
            MERGE (c1)-[:INHERITS]->(c2)
            """
            tx.run(query, batch=batch)
            
        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(internal_inheritance_batch), batch_size), desc="Internal Inherits"):
                    batch = internal_inheritance_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_internal_inheritance_tx, batch)
                        stats['inheritance_loaded'] += len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load internal inheritance batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load External Inheritance
        def load_external_inheritance_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (c1:Class {id: row.child_id})
            MERGE (e:ExternalClass {id: row.base_id})
            ON CREATE SET e.name = row.base_name
            MERGE (c1)-[:INHERITS]->(e)
            """
            tx.run(query, batch=batch)
            
        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(external_inheritance_batch), batch_size), desc="External Inherits"):
                    batch = external_inheritance_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_external_inheritance_tx, batch)
                        stats['inheritance_loaded'] += len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load external inheritance batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")
            
        # Load Functions
        def load_functions_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (f:File {path: row.path})
            MERGE (fn:Function {id: row.id})
            SET fn.name = row.name, fn.fqn = row.fqn, fn.signature = row.signature, fn.return_type = row.return_type, 
                fn.documentation = row.documentation, fn.line_number = row.line_number
            MERGE (f)-[:CONTAINS]->(fn)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(function_batch), batch_size), desc="Functions"):
                    batch = function_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_functions_tx, batch)
                        stats['functions_loaded'] = stats.get('functions_loaded', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load function batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load Internal Methods
        def load_internal_methods_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (c) WHERE (c:Class OR c:Struct) AND c.id = row.class_id
            MERGE (m:Method {id: row.id})
            SET m.name = row.name, m.fqn = row.fqn, m.signature = row.signature, m.return_type = row.return_type, 
                m.documentation = row.documentation, m.line_number = row.line_number
            MERGE (c)-[:HAS_METHOD]->(m)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(internal_method_batch), batch_size), desc="Internal Methods"):
                    batch = internal_method_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_internal_methods_tx, batch)
                        stats['methods_loaded'] = stats.get('methods_loaded', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load method batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load External Methods
        def load_external_methods_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (e:ExternalClass {id: row.class_name})
            ON CREATE SET e.name = row.class_name
            MERGE (m:Method {id: row.id})
            SET m.name = row.name, m.fqn = row.fqn, m.signature = row.signature, m.return_type = row.return_type, 
                m.documentation = row.documentation, m.line_number = row.line_number
            MERGE (e)-[:HAS_METHOD]->(m)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(external_method_batch), batch_size), desc="External Methods"):
                    batch = external_method_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_external_methods_tx, batch)
                        stats['methods_loaded'] = stats.get('methods_loaded', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load external method batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load Parameters
        def load_parameters_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (p:Parameter {id: row.id})
            SET p.name = row.name, p.type = row.type, p.position = row.position,
                p.default_value = row.default_value, p.is_const = row.is_const,
                p.is_pointer = row.is_pointer, p.is_reference = row.is_reference
            WITH row, p
            OPTIONAL MATCH (fn:Function {id: row.parent_id})
            OPTIONAL MATCH (m:Method {id: row.parent_id})
            WITH row, p, coalesce(fn, m) AS parent
            WHERE parent IS NOT NULL
            MERGE (parent)-[:HAS_PARAMETER]->(p)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(parameter_batch), batch_size), desc="Parameters"):
                    batch = parameter_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_parameters_tx, batch)
                        stats['parameters_loaded'] = stats.get('parameters_loaded', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load parameter batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load Uses Type
        def load_uses_type_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MATCH (p:Parameter {id: row.param_id})
            MATCH (c) WHERE (c:Class OR c:Struct OR c:Enum OR c:Typedef) AND c.id = row.class_id
            MERGE (p)-[:USES_TYPE]->(c)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(uses_type_batch), batch_size), desc="Uses Type"):
                    batch = uses_type_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_uses_type_tx, batch)
                        stats['uses_type_loaded'] = stats.get('uses_type_loaded', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load uses_type batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load Primitive Types
        def load_primitive_types_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (p:PrimitiveType {name: row.name})
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(primitive_type_batch), batch_size), desc="Primitive Types"):
                    batch = primitive_type_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_primitive_types_tx, batch)
                        stats['primitive_nodes_created'] = stats.get('primitive_nodes_created', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load primitive_type batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load External Types
        def load_external_types_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (e:ExternalType {name: row.name})
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(external_type_batch), batch_size), desc="External Types"):
                    batch = external_type_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_external_types_tx, batch)
                        stats['external_nodes_created'] = stats.get('external_nodes_created', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load external_type batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Load RETURNS Edges
        def load_returns_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            OPTIONAL MATCH (fn:Function {id: row.parent_id})
            OPTIONAL MATCH (m:Method {id: row.parent_id})
            WITH row, coalesce(fn, m) AS parent
            WHERE parent IS NOT NULL
            
            CALL (row, parent) {
                WITH row, parent
                WITH row, parent WHERE row.target_type = 'PrimitiveType'
                MATCH (t:PrimitiveType {name: row.name})
                MERGE (parent)-[:RETURNS]->(t)
                RETURN 1 AS n
                UNION
                WITH row, parent
                WITH row, parent WHERE row.target_type = 'ExternalType'
                MATCH (t:ExternalType {name: row.name})
                MERGE (parent)-[:RETURNS]->(t)
                RETURN 1 AS n
                UNION
                WITH row, parent
                WITH row, parent WHERE row.target_type = 'Class'
                MATCH (t) WHERE (t:Class OR t:Struct OR t:Enum OR t:Typedef) AND t.id = row.id
                MERGE (parent)-[:RETURNS]->(t)
                RETURN 1 AS n
            }
            RETURN count(*)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(returns_batch), batch_size), desc="RETURNS Edges"):
                    batch = returns_batch[i:i+batch_size]
                    try:
                        session.execute_write(load_returns_tx, batch)
                        stats['returns_loaded'] = stats.get('returns_loaded', 0) + len(batch)
                    except Exception as e:
                        logging.error(f"Failed to load returns batch: {e}")
                        stats['failures'] += 1
        except Exception as e:
            logging.error(f"Error: {e}")

        # Phase 5: Enums, EnumValues, Structs, Typedefs
        def load_enums_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (e:Enum {id: row.id})
            SET e.name = row.name, e.fqn = row.fqn, e.documentation = row.documentation, 
                e.line_number = row.line_number, e.file_path = row.file_path
            WITH row, e
            MATCH (f:File {path: row.file_path})
            MERGE (f)-[:CONTAINS]->(e)
            """
            tx.run(query, batch=batch)

        def load_enum_values_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (ev:EnumValue {id: row.id})
            SET ev.name = row.name, ev.value = row.value, ev.position = row.position
            WITH row, ev
            MATCH (e:Enum {id: row.parent_id})
            MERGE (e)-[:HAS_VALUE]->(ev)
            """
            tx.run(query, batch=batch)

        def load_structs_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (s:Struct {id: row.id})
            SET s.name = row.name, s.fqn = row.fqn, s.documentation = row.documentation, 
                s.line_number = row.line_number, s.file_path = row.file_path
            WITH row, s
            MATCH (f:File {path: row.file_path})
            MERGE (f)-[:CONTAINS]->(s)
            """
            tx.run(query, batch=batch)

        def load_typedefs_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (t:Typedef {id: row.id})
            SET t.name = row.name, t.fqn = row.fqn, t.target_type = row.target_type, 
                t.documentation = row.documentation, t.line_number = row.line_number, 
                t.file_path = row.file_path
            WITH row, t
            MATCH (f:File {path: row.file_path})
            MERGE (f)-[:CONTAINS]->(t)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(enum_batch), batch_size), desc="Enums"):
                    b = enum_batch[i:i+batch_size]
                    session.execute_write(load_enums_tx, b)
                    stats['enums_loaded'] += len(b)
                for i in tqdm(range(0, len(enum_value_batch), batch_size), desc="Enum Values"):
                    b = enum_value_batch[i:i+batch_size]
                    session.execute_write(load_enum_values_tx, b)
                    stats['enum_values_loaded'] += len(b)
                for i in tqdm(range(0, len(struct_batch), batch_size), desc="Structs"):
                    b = struct_batch[i:i+batch_size]
                    session.execute_write(load_structs_tx, b)
                    stats['structs_loaded'] += len(b)
                for i in tqdm(range(0, len(typedef_batch), batch_size), desc="Typedefs"):
                    b = typedef_batch[i:i+batch_size]
                    session.execute_write(load_typedefs_tx, b)
                    stats['typedefs_loaded'] += len(b)
        except Exception as e:
            logging.error(f"Error loading Phase 5: {e}")

        stats['parsed_enums'] = len(enum_batch)
        stats['parsed_enum_values'] = len(enum_value_batch)
        stats['parsed_structs'] = len(struct_batch)
        stats['parsed_typedefs'] = len(typedef_batch)
        
        # Phase 6: Documentation
        def load_documentation_tx(tx, batch):
            query = """
            UNWIND $batch AS row
            MERGE (d:Documentation {id: row.id})
            SET d.text = row.text, d.length = row.length, 
                d.entity_type = row.entity_type, d.entity_name = row.entity_name, 
                d.file_path = row.file_path
            WITH row, d
            CALL (row, d) {
                WITH row, d
                WITH row, d WHERE row.parent_label = 'Class'
                MATCH (e:Class {id: row.parent_id})
                MERGE (e)-[:HAS_DOC]->(d)
                RETURN 1 AS n
                UNION
                WITH row, d
                WITH row, d WHERE row.parent_label = 'Struct'
                MATCH (e:Struct {id: row.parent_id})
                MERGE (e)-[:HAS_DOC]->(d)
                RETURN 1 AS n
                UNION
                WITH row, d
                WITH row, d WHERE row.parent_label = 'Enum'
                MATCH (e:Enum {id: row.parent_id})
                MERGE (e)-[:HAS_DOC]->(d)
                RETURN 1 AS n
                UNION
                WITH row, d
                WITH row, d WHERE row.parent_label = 'Function'
                MATCH (e:Function {id: row.parent_id})
                MERGE (e)-[:HAS_DOC]->(d)
                RETURN 1 AS n
                UNION
                WITH row, d
                WITH row, d WHERE row.parent_label = 'Method'
                MATCH (e:Method {id: row.parent_id})
                MERGE (e)-[:HAS_DOC]->(d)
                RETURN 1 AS n
            }
            RETURN count(*)
            """
            tx.run(query, batch=batch)

        try:
            with self.driver.session() as session:
                for i in tqdm(range(0, len(doc_batch), batch_size), desc="Documentation"):
                    b = doc_batch[i:i+batch_size]
                    session.execute_write(load_documentation_tx, b)
                    stats['docs_loaded'] += len(b)
        except Exception as e:
            logging.error(f"Error loading Phase 6: {e}")

        stats['parsed_docs'] = len(doc_batch)

        # Load ACTIVE_IN_CONFIGURATION
        def load_active_in_config_tx(tx, batch, label):
            query = f"""
            UNWIND $batch AS row
            MATCH (e:{label} {{id: row.entity_id}})
            MATCH (b:BuildConfiguration {{name: row.config_name}})
            MERGE (e)-[:ACTIVE_IN_CONFIGURATION]->(b)
            """
            tx.run(query, batch=batch)

        if active_in_config_batch:
            logging.info("Starting ACTIVE_IN_CONFIGURATION relationships load...")
            by_type = {}
            for item in active_in_config_batch:
                by_type.setdefault(item['entity_type'], []).append(item)
                
            try:
                with self.driver.session() as session:
                    for label, items in by_type.items():
                        for i in range(0, len(items), batch_size):
                            batch = items[i:i+batch_size]
                            session.execute_write(load_active_in_config_tx, batch, label)
            except Exception as e:
                logging.error(f"Error during ACTIVE_IN_CONFIGURATION processing: {e}")
                stats['failures'] += 1

        stats['end_time'] = time.time()
        
        # Calculate exactly how many JSON instances had duplicate IDs purely by data
        # Even with full signatures, if the EXACT same signature is in the EXACT same file,
        # it counts as a duplicate ID. This means the parser extracted it twice.
        func_ids = set()
        method_ids = set()
        for b in function_batch: func_ids.add(b['id'])
        for b in internal_method_batch: method_ids.add(b['id'])
        for b in external_method_batch: method_ids.add(b['id'])
        
        stats['unique_function_ids_in_json'] = len(func_ids)
        stats['unique_method_ids_in_json'] = len(method_ids)
        
        # Calculate lookup failures for report
        stats['class_lookup_failures'] = len(external_method_batch)
        
        return stats

    def validate_graph(self):
        if not self.driver:
            return None
        validation = {}
        try:
            with self.driver.session() as session:
                validation['total_files'] = session.run("MATCH (f:File) RETURN count(f) AS count").single()['count']
                validation['total_classes'] = session.run("MATCH (c:Class) RETURN count(c) AS count").single()['count']
                validation['total_external_classes'] = session.run("MATCH (e:ExternalClass) RETURN count(e) AS count").single()['count']
                validation['total_inherits'] = session.run("MATCH ()-[r:INHERITS]->() RETURN count(r) AS count").single()['count']
                
                validation['total_functions'] = session.run("MATCH (fn:Function) RETURN count(fn) AS count").single()['count']
                validation['total_methods'] = session.run("MATCH (m:Method) RETURN count(m) AS count").single()['count']
                validation['total_file_contains_func'] = session.run("MATCH (:File)-[r:CONTAINS]->(:Function) RETURN count(r) AS count").single()['count']
                validation['total_class_has_method'] = session.run("MATCH ()-[r:HAS_METHOD]->(:Method) RETURN count(r) AS count").single()['count']
                
                # Phase 3 Validation
                validation['total_parameters'] = session.run("MATCH (p:Parameter) RETURN count(p) AS count").single()['count']
                validation['duplicate_parameters'] = session.run("MATCH (p:Parameter) WITH p.id AS id, count(*) AS c WHERE c > 1 RETURN count(id) AS count").single()['count']
                validation['orphan_parameters'] = session.run("MATCH (p:Parameter) WHERE NOT EXISTS { MATCH ()-[:HAS_PARAMETER]->(p) } RETURN count(p) AS count").single()['count']
                validation['total_uses_type'] = session.run("MATCH (:Parameter)-[r:USES_TYPE]->(:Class) RETURN count(r) AS count").single()['count']
                validation['total_has_parameter'] = session.run("MATCH ()-[r:HAS_PARAMETER]->(:Parameter) RETURN count(r) AS count").single()['count']
                
                # Phase 4 Validation
                validation['total_primitive_types'] = session.run("MATCH (p:PrimitiveType) RETURN count(p) AS count").single()['count']
                validation['total_external_types'] = session.run("MATCH (e:ExternalType) RETURN count(e) AS count").single()['count']
                validation['total_returns_edges'] = session.run("MATCH ()-[r:RETURNS]->() RETURN count(r) AS count").single()['count']
                validation['returns_class_edges'] = session.run("MATCH ()-[r:RETURNS]->(:Class) RETURN count(r) AS count").single()['count']
                validation['returns_primitive_edges'] = session.run("MATCH ()-[r:RETURNS]->(:PrimitiveType) RETURN count(r) AS count").single()['count']
                validation['returns_external_edges'] = session.run("MATCH ()-[r:RETURNS]->(:ExternalType) RETURN count(r) AS count").single()['count']
                
                # Check for orphans
                fn_count = session.run("MATCH (f:Function) RETURN count(f) AS count").single()['count']
                m_count = session.run("MATCH (m:Method) RETURN count(m) AS count").single()['count']
                fn_with_returns = session.run("MATCH (f:Function)-[:RETURNS]->() RETURN count(f) AS count").single()['count']
                m_with_returns = session.run("MATCH (m:Method)-[:RETURNS]->() RETURN count(m) AS count").single()['count']
                validation['orphan_returns_edges'] = (fn_count - fn_with_returns) + (m_count - m_with_returns)
                
                # Return Type Stats
                stats_query = """
                MATCH (n)-[:RETURNS]->(t)
                RETURN 
                    CASE 
                        WHEN 'Class' IN labels(t) THEN t.name 
                        WHEN 'PrimitiveType' IN labels(t) THEN t.name 
                        WHEN 'ExternalType' IN labels(t) THEN t.name 
                    END AS type_name, count(*) AS freq
                ORDER BY freq DESC LIMIT 50
                """
                validation['top_return_types'] = session.run(stats_query).data()
                
                # Phase 5 Validation
                validation['total_enums'] = session.run("MATCH (e:Enum) RETURN count(e) AS count").single()['count']
                validation['total_enum_values'] = session.run("MATCH (ev:EnumValue) RETURN count(ev) AS count").single()['count']
                validation['total_structs'] = session.run("MATCH (s:Struct) RETURN count(s) AS count").single()['count']
                validation['total_typedefs'] = session.run("MATCH (t:Typedef) RETURN count(t) AS count").single()['count']
                validation['total_has_value_edges'] = session.run("MATCH ()-[r:HAS_VALUE]->() RETURN count(r) AS count").single()['count']
                validation['total_aliases_edges'] = session.run("MATCH ()-[r:ALIASES]->() RETURN count(r) AS count").single()['count']
                
                # Check for orphans
                validation['orphan_enums'] = session.run("MATCH (e:Enum) WHERE NOT EXISTS { MATCH ()-[:CONTAINS]->(e) } RETURN count(e) AS count").single()['count']
                validation['orphan_enum_values'] = session.run("MATCH (ev:EnumValue) WHERE NOT EXISTS { MATCH ()-[:HAS_VALUE]->(ev) } RETURN count(ev) AS count").single()['count']
                validation['orphan_structs'] = session.run("MATCH (s:Struct) WHERE NOT EXISTS { MATCH ()-[:CONTAINS]->(s) } RETURN count(s) AS count").single()['count']
                validation['orphan_typedefs'] = session.run("MATCH (t:Typedef) WHERE NOT EXISTS { MATCH ()-[:CONTAINS]->(t) } RETURN count(t) AS count").single()['count']
                
                # Check for duplicates
                validation['duplicate_enums'] = session.run("MATCH (e:Enum) WITH e.id AS id, count(*) AS c WHERE c > 1 RETURN count(id) AS count").single()['count']
                validation['duplicate_enum_values'] = session.run("MATCH (ev:EnumValue) WITH ev.id AS id, count(*) AS c WHERE c > 1 RETURN count(id) AS count").single()['count']
                validation['duplicate_structs'] = session.run("MATCH (s:Struct) WITH s.id AS id, count(*) AS c WHERE c > 1 RETURN count(id) AS count").single()['count']
                validation['duplicate_typedefs'] = session.run("MATCH (t:Typedef) WITH t.id AS id, count(*) AS c WHERE c > 1 RETURN count(id) AS count").single()['count']
                
                # Phase 6 Validation
                validation['total_docs'] = session.run("MATCH (d:Documentation) RETURN count(d) AS count").single()['count']
                validation['class_docs'] = session.run("MATCH (:Class)-[:HAS_DOC]->(d:Documentation) RETURN count(d) AS count").single()['count']
                validation['struct_docs'] = session.run("MATCH (:Struct)-[:HAS_DOC]->(d:Documentation) RETURN count(d) AS count").single()['count']
                validation['enum_docs'] = session.run("MATCH (:Enum)-[:HAS_DOC]->(d:Documentation) RETURN count(d) AS count").single()['count']
                validation['function_docs'] = session.run("MATCH (:Function)-[:HAS_DOC]->(d:Documentation) RETURN count(d) AS count").single()['count']
                validation['method_docs'] = session.run("MATCH (:Method)-[:HAS_DOC]->(d:Documentation) RETURN count(d) AS count").single()['count']
                
                validation['has_doc_edges'] = session.run("MATCH ()-[r:HAS_DOC]->() RETURN count(r) AS count").single()['count']
                
                validation['avg_doc_length'] = session.run("MATCH (d:Documentation) RETURN avg(d.length) AS val").single()['val'] or 0
                validation['max_doc_length'] = session.run("MATCH (d:Documentation) RETURN max(d.length) AS val").single()['val'] or 0
                validation['min_doc_length'] = session.run("MATCH (d:Documentation) RETURN min(d.length) AS val").single()['val'] or 0
                
                validation['orphan_docs'] = session.run("MATCH (d:Documentation) WHERE NOT ()-[:HAS_DOC]->(d) RETURN count(d) AS count").single()['count']
                validation['duplicate_docs'] = session.run("MATCH (d:Documentation) WITH d.id AS id, count(*) AS c WHERE c > 1 RETURN count(id) AS count").single()['count']
                
        except Exception as e:
            logging.error(f"Validation failed: {e}")
            
        return validation

def generate_report(stats, validation):
    report = f"# ACIS Knowledge Graph Phase 6 - Validation Report\n\n"
    report += f"## Execution Summary\n"
    if stats:
        duration = stats.get('end_time', 0) - stats.get('start_time', 0)
        report += f"- **Start Time:** {time.ctime(stats.get('start_time'))}\n"
        report += f"- **End Time:** {time.ctime(stats.get('end_time'))}\n"
        report += f"- **Execution Time:** {duration:.2f} seconds\n"
        report += f"- **Errors Encountered:** {stats.get('failures', 0)}\n\n"
        
        report += f"## Data Processed (from JSON)\n"
        report += f"- Documentation parsed: {stats.get('parsed_docs', 0)}\n"
        report += f"- Documentation loaded: {stats.get('docs_loaded', 0)}\n"
        
    else:
        report += "Graph build did not execute successfully.\n\n"
        
    report += f"## Validation Results (Neo4j Graph Database)\n"
    if validation:
        report += f"- **Documentation Nodes Created:** {validation.get('total_docs', 0)}\n"
        report += f"- **HAS_DOC Relationships Created:** {validation.get('has_doc_edges', 0)}\n\n"
        
        report += f"### Documentation by Entity Type\n"
        report += f"- **Class Docs:** {validation.get('class_docs', 0)}\n"
        report += f"- **Struct Docs:** {validation.get('struct_docs', 0)}\n"
        report += f"- **Enum Docs:** {validation.get('enum_docs', 0)}\n"
        report += f"- **Function Docs:** {validation.get('function_docs', 0)}\n"
        report += f"- **Method Docs:** {validation.get('method_docs', 0)}\n\n"
        
        report += f"### Documentation Length Metrics\n"
        report += f"- **Average Length:** {validation.get('avg_doc_length', 0):.2f} chars\n"
        report += f"- **Longest Length:** {validation.get('max_doc_length', 0)} chars\n"
        report += f"- **Shortest Length:** {validation.get('min_doc_length', 0)} chars\n\n"
        
        report += f"### Integrity Checks\n"
        report += f"- **Orphan Documentation Nodes:** {validation.get('orphan_docs', 0)}\n"
        report += f"- **Duplicate Documentation IDs:** {validation.get('duplicate_docs', 0)}\n\n"
        
    else:
        report += "Validation queries failed.\n\n"
        
    with open('phase6_validation_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print("Report written to phase6_validation_report.md")

    if stats and validation:
        # Phase 6 Certification Checks
        passed = True
        reasons = []
        
        if validation.get('total_docs', 0) == 0:
            passed = False
            reasons.append("Documentation Nodes == 0 (Expected > 0)")
        if validation.get('has_doc_edges', 0) == 0:
            passed = False
            reasons.append("HAS_DOC edges == 0 (Expected > 0)")
        if validation.get('orphan_docs', -1) != 0:
            passed = False
            reasons.append(f"Orphan Documentation Nodes == {validation.get('orphan_docs')} (Expected 0)")
        if validation.get('duplicate_docs', -1) != 0:
            passed = False
            reasons.append(f"Duplicate Documentation IDs == {validation.get('duplicate_docs')} (Expected 0)")
        if stats.get('failures', -1) != 0:
            passed = False
            reasons.append(f"Errors == {stats.get('failures')} (Expected 0)")
            
        doc_nodes = validation.get('total_docs', 0)
        doc_edges = validation.get('has_doc_edges', 0)
        parsed_docs = stats.get('parsed_docs', 0)
        
        if abs(doc_nodes - doc_edges) > max(5, int(doc_nodes * 0.01)):
            passed = False
            reasons.append(f"Mismatch: Documentation Nodes ({doc_nodes}) != HAS_DOC edges ({doc_edges})")
            
        if abs(doc_nodes - parsed_docs) > max(5, int(parsed_docs * 0.01)):
            passed = False
            reasons.append(f"Load mismatch: DB({doc_nodes}) != JSON({parsed_docs})")
            
        with open('phase6_certification.md', 'w', encoding='utf-8') as f:
            f.write("# Phase 6 Certification\n\n")
            if passed:
                f.write("## Status: PASSED\n\n")
                f.write("All certification checks passed successfully.\n\n")
            else:
                f.write("## Status: FAILED\n\n")
                f.write("The following checks failed:\n")
                for r in reasons:
                    f.write(f"- {r}\n")
            f.write("### Metrics:\n")
            f.write(f"- Documentation Nodes: {validation.get('total_docs', 0)}\n")
            f.write(f"- HAS_DOC edges: {validation.get('has_doc_edges', 0)}\n")
            f.write(f"- Orphan Docs: {validation.get('orphan_docs', 0)}\n")
        print("Certification report written to phase6_certification.md")

if __name__ == '__main__':
    logging.info("Starting Graph Build Phase 2B")
    
    # Read credentials from environment variables, or use defaults
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    USER = os.getenv("NEO4J_USER", "neo4j")
    PASSWORD = os.getenv("NEO4J_PASSWORD", "nadeed@3973")
    
    print(f"Connecting to Neo4j at {URI}...")
    builder = KnowledgeGraphBuilder(URI, USER, PASSWORD)
    if builder.driver:
        print("Resetting database (Phase 2C full rebuild)...")
        builder.reset_database()
        
        print("Creating identity constraints...")
        builder.create_constraints()
        
        print("Loading JSON data...")
        data = builder.load_data('code_base.json')
        if data:
            print("Data loaded. Starting graph build...")
            stats = builder.build_graph(data)
            
            print("Graph build completed. Compiling and loading Call Graph...")
            from call_graph_builder import CallGraphBuilder
            call_builder = CallGraphBuilder(URI, USER, PASSWORD)
            call_builder.load_calls(data)
            call_builder.close()
            
            print("Call Graph loaded. Validating Neo4j graph...")
            validation = builder.validate_graph()
            generate_report(stats, validation)
        builder.close()
    else:
        logging.error("Exiting due to connection failure.")
        # Generate partial report
        generate_report(None, None)
