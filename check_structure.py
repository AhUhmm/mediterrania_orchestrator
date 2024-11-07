import os

def check_project_structure():
    base_dir = "."
    expected_structure = {
        "src": {
            "mediterrania_orchestrator": {
                "__init__.py": "file",
                "core": {
                    "__init__.py": "file",
                    "orchestrator.py": "file",
                    "nutritional_verifier.py": "file",
                    "substitution_handler.py": "file"
                },
                "database": {
                    "__init__.py": "file",
                    "database_handler.py": "file"
                },
                "utils": {
                    "__init__.py": "file",
                    "logger.py": "file"
                }
            },
            "__init__.py": "file"
        }
    }

    def check_structure(directory, structure, path=""):
        missing = []
        for name, kind in structure.items():
            full_path = os.path.join(path, name)
            if isinstance(kind, dict):
                if not os.path.isdir(os.path.join(directory, full_path)):
                    missing.append(f"Missing directory: {full_path}")
                else:
                    missing.extend(check_structure(directory, kind, full_path))
            else:  # file
                if not os.path.isfile(os.path.join(directory, full_path)):
                    missing.append(f"Missing file: {full_path}")
        return missing

    missing_items = check_structure(base_dir, expected_structure)
    
    if missing_items:
        print("Missing items:")
        for item in missing_items:
            print(item)
    else:
        print("All files and directories are present!")

if __name__ == "__main__":
    check_project_structure()