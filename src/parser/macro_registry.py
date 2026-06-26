class MacroRegistry:
    def __init__(self, cmd_line_macros=None):
        self.global_macros = cmd_line_macros or {}
        self.file_macros = {}

    def clear_file_macros(self):
        self.file_macros = {}

    def define(self, name, value="1"):
        self.file_macros[name] = value

    def undefine(self, name):
        if name in self.file_macros:
            del self.file_macros[name]
        # Undefining command line macro for the file
        elif name in self.global_macros:
            self.file_macros[name] = None # Shadow to mark as undefined

    def is_defined(self, name):
        # File-specific macro or shadow takes precedence
        if name in self.file_macros:
            return self.file_macros[name] is not None
        return name in self.global_macros

    def get_value(self, name):
        if name in self.file_macros:
            val = self.file_macros[name]
            return val if val is not None else "0"
        return self.global_macros.get(name, "0")
