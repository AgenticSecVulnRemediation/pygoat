import ast


def _find_function_def(module_ast: ast.AST, name: str) -> ast.FunctionDef:
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Function {name} not found")


def test_a9_lab_uses_yaml_safe_load_not_yaml_load():
    """Delta: a9_lab uses yaml.safe_load(file) instead of yaml.load(file, yaml.Loader)."""
    src = open('introduction/views.py', 'r', encoding='utf-8').read()
    module_ast = ast.parse(src)

    fn = _find_function_def(module_ast, 'a9_lab')

    safe_load_calls = [
        n for n in ast.walk(fn)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == 'yaml'
        and n.func.attr == 'safe_load'
    ]
    assert safe_load_calls, 'Expected yaml.safe_load(...) call in a9_lab'

    load_calls = [
        n for n in ast.walk(fn)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == 'yaml'
        and n.func.attr == 'load'
    ]
    assert not load_calls, 'Did not expect yaml.load(...) call in a9_lab'
