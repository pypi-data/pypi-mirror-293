import ast
import astor

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
            if (func_name in self.supported_functions and
                    any(keyword.arg in self.modifications for keyword in node.keywords)):
                for keyword in node.keywords:
                    if keyword.arg in self.modifications:
                        new_value = self.modifications[keyword.arg]
                        if isinstance(new_value, str):
                            keyword.value = ast.Constant(value=new_value)
                        elif isinstance(new_value, (int, float)):
                            keyword.value = ast.Constant(value=new_value)
        return self.generic_visit(node)
