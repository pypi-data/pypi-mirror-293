import sys
from .utils import load_supported_functions, modify_script, execute_script

def main():
    if len(sys.argv) < 2 or "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: tuneX <script.py> param1=value1 param2=value2 ...")
        sys.exit(0)

    script_path = sys.argv[1]

    if not script_path.endswith('.py'):
        print("Error: The first argument must be a Python script file (with a .py extension).")
        sys.exit(1)

    modifications = {}
    for param in sys.argv[2:]:
        key, value = param.split('=')
        modifications[key] = int(value) if value.isdigit() else float(value) if '.' in value else value

    supported_functions = load_supported_functions()  # Default to functions.txt
    modified_code = modify_script(script_path, modifications, supported_functions)
    execute_script(modified_code)

if __name__ == "__main__":
    main()
