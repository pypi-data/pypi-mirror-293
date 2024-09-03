def load_supported_functions(file_path='functions.txt'):
    with open(file_path, 'r') as file:
        functions = {line.strip() for line in file if line.strip()}
    return functions

def modify_script(script_path, modifications, supported_functions):
    import ast
    import astor
    from .script_modifier import ScriptModifier

    with open(script_path, 'r') as file:
        tree = ast.parse(file.read(), filename=script_path)

    modifier = ScriptModifier(modifications, supported_functions)
    tree = modifier.visit(tree)
    ast.fix_missing_locations(tree)

    modified_code_str = astor.to_source(tree)
    print(f"Modified Code for {script_path}:\n{modified_code_str}")
    
    return modified_code_str

def execute_script(script_code):
    print("Modifications applied. Running....")
    exec_globals = {}
    exec(script_code, exec_globals)
