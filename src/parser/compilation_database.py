import json
import os
import shlex

class CompilationDatabase:
    def __init__(self, file_path=None):
        self.entries = {}
        if file_path and os.path.exists(file_path):
            self.load(file_path)

    def load(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.entries = {}
        for entry in data:
            file_name = entry.get("file", "")
            directory = entry.get("directory", "")
            # Canonicalize path relative to entry directory
            file_abs = os.path.abspath(os.path.join(directory, file_name)).replace("\\", "/")
            
            # Extract arguments
            command = entry.get("command", "")
            arguments = entry.get("arguments", [])
            if not arguments and command:
                arguments = shlex.split(command)
                
            self.entries[file_abs] = {
                "directory": directory,
                "arguments": arguments,
                "file": file_name
            }

    def get_info(self, file_path):
        abs_path = os.path.abspath(file_path).replace("\\", "/")
        # Try direct match
        if abs_path in self.entries:
            return self.entries[abs_path]
            
        # Try matching by filename only if exact path doesn't match
        base = os.path.basename(abs_path)
        for path, info in self.entries.items():
            if os.path.basename(path) == base:
                return info
        return None

    def extract_flags(self, info):
        if not info:
            return {
                "includes": [],
                "macros": {},
                "std": None,
                "compiler": None
            }
            
        arguments = info["arguments"]
        directory = info["directory"]
        
        includes = []
        macros = {}
        std = None
        compiler = None
        
        if arguments:
            compiler = os.path.basename(arguments[0])
            
        i = 1
        while i < len(arguments):
            arg = arguments[i]
            
            # Standard
            if arg.startswith("-std=") or arg.startswith("--std="):
                std = arg.split("=")[1]
            elif arg.startswith("/std:"):
                std = arg.split(":")[1]
                
            # Include paths
            elif arg.startswith("-I") or arg.startswith("/I"):
                path = arg[2:]
                if not path and i + 1 < len(arguments):
                    i += 1
                    path = arguments[i]
                if path:
                    # Resolve relative to directory
                    abs_include = os.path.abspath(os.path.join(directory, path)).replace("\\", "/")
                    includes.append(abs_include)
                    
            elif arg.startswith("-isystem"):
                path = arg[8:]
                if not path and i + 1 < len(arguments):
                    i += 1
                    path = arguments[i]
                if path:
                    abs_include = os.path.abspath(os.path.join(directory, path)).replace("\\", "/")
                    includes.append(abs_include)
                    
            # Macro definitions
            elif arg.startswith("-D") or arg.startswith("/D"):
                macro_def = arg[2:]
                if not macro_def and i + 1 < len(arguments):
                    i += 1
                    macro_def = arguments[i]
                if macro_def:
                    if "=" in macro_def:
                        name, val = macro_def.split("=", 1)
                        macros[name] = val
                    else:
                        macros[macro_def] = "1"
            i += 1
            
        return {
            "includes": list(dict.fromkeys(includes)), # Deduplicate preserving order
            "macros": macros,
            "std": std,
            "compiler": compiler
        }
