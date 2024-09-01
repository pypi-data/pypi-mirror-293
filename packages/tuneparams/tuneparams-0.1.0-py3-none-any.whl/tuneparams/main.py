import ast
import astor
import sys

class ScriptModifier(ast.NodeTransformer):
    def __init__(self, modifications, supported_functions):
        self.modifications = modifications
        self.supported_functions = supported_functions

    def visit_FunctionDef(self, node):
        for i, default in enumerate(node.args.defaults):
            if i < len(node.args.args):
                arg_name = node.args.args[-len(node.args.defaults) + i].arg
                if arg_name in self.modifications:
                    new_value = self.modifications[arg_name]
                    if isinstance(new_value, str):
                        node.args.defaults[i] = ast.Constant(value=new_value)
                    elif isinstance(new_value, (int, float)):
                        node.args.defaults[i] = ast.Constant(value=new_value)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float, str)):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in self.modifications:
                    new_value = self.modifications[target.id]
                    if isinstance(new_value, str):
                        node.value = ast.Constant(value=new_value)
                    elif isinstance(new_value, (int, float)):
                        node.value = ast.Constant(value=new_value)
        return self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in self.supported_functions:
                for i, keyword in enumerate(node.keywords):
                    if keyword.arg in self.modifications:
                        new_value = self.modifications[keyword.arg]
                        if isinstance(new_value, str):
                            keyword.value = ast.Constant(value=new_value)
                        elif isinstance(new_value, (int, float)):
                            keyword.value = ast.Constant(value=new_value)
        return self.generic_visit(node)

def load_supported_functions(file_path='functions.txt'):
    with open(file_path, 'r') as file:
        functions = {line.strip() for line in file if line.strip()}
    return functions

def modify_script(script_path, modifications, supported_functions):
    with open(script_path, 'r') as file:
        tree = ast.parse(file.read(), filename=script_path)

    modifier = ScriptModifier(modifications, supported_functions)
    tree = modifier.visit(tree)
    ast.fix_missing_locations(tree)

    modified_code_str = astor.to_source(tree)
    print(f"Modified Code for {script_path}:\n{modified_code_str}")
    
    return modified_code_str

def execute_script(script_code):
    print("Modifications applied. Running....\n")
    exec_globals = {}
    exec(script_code, exec_globals)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <script.py> param1=value1 param2=value2 ...")
        sys.exit(1)

    script_path = sys.argv[1]
    modifications = {}

    for param in sys.argv[2:]:
        key, value = param.split('=')
        modifications[key] = int(value) if value.isdigit() else float(value) if '.' in value else value

    supported_functions = load_supported_functions()  # Default to functions.txt
    modified_code = modify_script(script_path, modifications, supported_functions)
    execute_script(modified_code)

if __name__ == "__main__":
    main()
