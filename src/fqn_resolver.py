import re

# Primitive types list to avoid unresolved prefix
PRIMITIVE_TYPES = {
    'int', 'double', 'float', 'bool', 'char', 'void', 'size_t', 'long', 'short', 
    'unsigned', 'signed', 'unsigned int', 'unsigned long', 'char*', 'const char*'
}

def clean_type_name(name):
    if not name:
        return ""
    name = re.sub(r'//.*', '', name)
    name = re.sub(r'/\*.*?\*/', '', name, flags=re.DOTALL)
    name = name.replace("class ", "").replace("struct ", "").replace("typename ", "").strip()
    return name

def get_canonical_key(type_str):
    """
    Get canonical name of type by removing templates, pointers, and references.
    E.g. "const std::vector<int>&" -> "std::vector"
    """
    cleaned = clean_type_name(type_str)
    # Strip const qualifiers from beginning and end
    cleaned = re.sub(r'^\s*const\s+', '', cleaned)
    cleaned = re.sub(r'\s+const\s*$', '', cleaned)
    # Strip pointer/reference
    cleaned = cleaned.replace("*", "").replace("&", "").strip()
    # Strip templates
    if "<" in cleaned:
        cleaned = cleaned.split("<")[0].strip()
    return cleaned

class FQNResolver:
    def __init__(self, global_type_index=None):
        # global_type_index maps canonical_key -> list of defined FQNs
        self.global_type_index = global_type_index or {}

    def build_index(self, parsed_data):
        """
        Builds the global type index from parsed files dataset.
        parsed_data is a list of file dictionaries.
        """
        self.global_type_index = {}
        for item in parsed_data:
            # Classes
            for c in item.get("classes", []):
                fqn = c.get("fqn")
                if fqn:
                    self._add_to_index(fqn)
            # Structs
            for s in item.get("structs", []):
                fqn = s.get("fqn")
                if fqn:
                    self._add_to_index(fqn)
            # Enums
            for e in item.get("enums", []):
                fqn = e.get("fqn")
                if fqn:
                    self._add_to_index(fqn)
            # Typedefs
            for t in item.get("typedefs", []):
                fqn = t.get("fqn")
                if fqn:
                    self._add_to_index(fqn)
            # Functions & Methods
            for f in item.get("functions", []):
                name = f.get("name")
                class_owner = f.get("class_owner")
                namespaces = f.get("namespaces", [])
                if name:
                    if class_owner:
                        fqn = f"{class_owner}::{name}"
                    else:
                        scope_str = "::".join(namespaces)
                        fqn = f"{scope_str}::{name}" if scope_str else name
                    self._add_to_index(fqn)

    def _add_to_index(self, fqn):
        key = fqn.split("::")[-1]
        if key not in self.global_type_index:
            self.global_type_index[key] = []
        if fqn not in self.global_type_index[key]:
            self.global_type_index[key].append(fqn)

    def resolve_type_fqn(self, type_str, scope_namespaces, scope_classes):
        """
        Resolve a parameter/return typename to its FQN using proximity heuristics.
        """
        canonical = get_canonical_key(type_str)
        if not canonical:
            return "unresolved::void"
            
        if canonical in PRIMITIVE_TYPES:
            return canonical

        # If it already contains explicit qualification (e.g. std::vector or acis::topology::BODY)
        if "::" in canonical:
            # Let's check if the first part exists in index or if we can resolve the base part
            parts = canonical.split("::")
            base_key = parts[-1]
            if base_key in self.global_type_index:
                # Find matching FQN that ends with canonical
                for fqn in self.global_type_index[base_key]:
                    if fqn.endswith(canonical):
                        return fqn
            # If not in index, it's explicitly qualified but not defined, keep it as is
            return canonical

        # Look up candidates in index
        candidates = self.global_type_index.get(canonical, [])
        if not candidates:
            return f"unresolved::{canonical}"

        if len(candidates) == 1:
            return candidates[0]

        # Multiple candidates: Rank by proximity
        best_candidate = None
        best_score = -1
        
        scope_path = scope_namespaces + scope_classes
        for cand in candidates:
            cand_parts = cand.split("::")[:-1]
            # Calculate prefix match count
            score = 0
            for cp, sp in zip(cand_parts, scope_path):
                if cp == sp:
                    score += 1
                else:
                    break
            
            # Additional heuristic: if candidate is defined in the same namespace group
            # (e.g. sharing any parts)
            shared_parts = set(cand_parts).intersection(set(scope_namespaces))
            score += len(shared_parts) * 0.1
            
            if score > best_score:
                best_score = score
                best_candidate = cand

        return best_candidate or candidates[0]

    def resolve_query_short_name(self, short_name):
        """
        Resolve a user query short name to its best FQN candidate.
        """
        canonical = get_canonical_key(short_name)
        candidates = self.global_type_index.get(canonical, [])
        if not candidates:
            # Return list of potential fuzzy matches or fallback
            # Let's check all keys for sub-match
            matches = []
            for key, fqns in self.global_type_index.items():
                if canonical.lower() in key.lower():
                    matches.extend(fqns)
            return matches if matches else [short_name]
        return candidates
