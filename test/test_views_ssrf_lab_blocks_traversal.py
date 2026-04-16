import ast


def _find_function_def(module_ast: ast.AST, name: str) -> ast.FunctionDef:
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Function {name} not found")


def test_ssrf_lab_blocks_dotdot_and_abs_path():
    """Delta: ssrf_lab rejects '..' and absolute paths before opening file."""
    src = open('introduction/views.py', 'r', encoding='utf-8').read()
    module_ast = ast.parse(src)

    fn = _find_function_def(module_ast, 'ssrf_lab')

    # Check presence of os.path.isabs(file) usage
    assert any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and isinstance(n.func.value, ast.Attribute)
        and isinstance(n.func.value.value, ast.Name)
        and n.func.value.value.id == 'os'
        and n.func.value.attr == 'path'
        and n.func.attr == 'isabs'
        for n in ast.walk(fn)
    ), 'Expected os.path.isabs(file) check'

    # Check presence of '..' constant in a comparison/containment check
    assert any(
        isinstance(n, ast.Constant) and n.value == '..'
        for n in ast.walk(fn)
    ), "Expected '..' constant in ssrf_lab"
