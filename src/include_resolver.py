import os

class IncludeResolver:
    def __init__(self, include_dirs=None, repo_root=None):
        self.include_dirs = include_dirs or []
        self.repo_root = repo_root
        self.file_cache = {}
        if repo_root:
            self._build_file_cache(repo_root)

    def _build_file_cache(self, repo_root):
        """
        Builds a map of basename -> absolute path for fallback resolver search.
        """
        for root, _, files in os.walk(repo_root):
            for file in files:
                path = os.path.abspath(os.path.join(root, file)).replace("\\", "/")
                self.file_cache[file] = path
                self.file_cache[file.lower()] = path

    def resolve(self, include_target, current_file_path, is_angled=False):
        """
        Resolves include_target (e.g. 'helper.h') to its absolute path.
        """
        dirs_to_search = []
        
        # 1. Quote includes search the current file's directory first
        if not is_angled and current_file_path:
            dirs_to_search.append(os.path.dirname(os.path.abspath(current_file_path)))
            
        # 2. Add compiler include paths
        for d in self.include_dirs:
            dirs_to_search.append(os.path.abspath(d))
            
        # Try finding the file in search directories
        for d in dirs_to_search:
            candidate = os.path.abspath(os.path.join(d, include_target)).replace("\\", "/")
            if os.path.exists(candidate) and os.path.isfile(candidate):
                return candidate
                
        # 3. Fallback: Search using workspace file cache
        basename = os.path.basename(include_target)
        if basename in self.file_cache:
            return self.file_cache[basename]
        if basename.lower() in self.file_cache:
            return self.file_cache[basename.lower()]
            
        return None
