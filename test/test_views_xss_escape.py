import ast


def _find_function_def(module_ast: ast.AST, name: str) -> ast.FunctionDef:
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Function {name} not found")


def _first_assignment_call_name(func_def: ast.FunctionDef, var_name: str) -> str:
    for node in func_def.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == var_name for t in node.targets):
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                return node.value.func.id
            return "<non-call>"
    return "<missing>"


def test_xss_lab2_uses_escape_on_username_assignment():
    src = open('introduction/views.py', 'r', encoding='utf-8').read()
    module_ast = ast.parse(src)

    fn = _find_function_def(module_ast, 'xss_lab2')
    call_name = _first_assignment_call_name(fn, 'username')

    assert call_name == 'escape'


def test_xss_lab3_uses_escape_on_username_assignment():
    src = open('introduction/views.py', 'r', encoding='utf-8').read()
    module_ast = ast.parse(src)

    fn = _find_function_def(module_ast, 'xss_lab3')
    call_name = _first_assignment_call_name(fn, 'username')

    assert call_name == 'escape'
