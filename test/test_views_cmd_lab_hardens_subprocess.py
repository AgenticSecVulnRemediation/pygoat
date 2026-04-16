import ast


def _find_function_def(module_ast: ast.AST, name: str) -> ast.FunctionDef:
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Function {name} not found")


def test_cmd_lab_validates_domain_and_uses_list_command_and_no_shell_true():
    """Delta: cmd_lab validates domain with regex, builds argv list, and no longer uses shell=True."""
    src = open('introduction/views.py', 'r', encoding='utf-8').read()
    module_ast = ast.parse(src)

    fn = _find_function_def(module_ast, 'cmd_lab')

    # Ensure regex validation exists
    assert any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == 're'
        and n.func.attr == 'match'
        for n in ast.walk(fn)
    ), 'Expected re.match(...) validation in cmd_lab'

    # Ensure subprocess.Popen is called with command as Name (list variable) or list literal,
    # and without shell=True keyword.
    popen_calls = [
        n for n in ast.walk(fn)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == 'subprocess'
        and n.func.attr == 'Popen'
    ]
    assert popen_calls, 'Expected subprocess.Popen call in cmd_lab'

    for call in popen_calls:
        assert not any(isinstance(kw, ast.keyword) and kw.arg == 'shell' for kw in call.keywords), 'shell kwarg should not be present'

        cmd_arg = call.args[0] if call.args else None
        assert isinstance(cmd_arg, (ast.List, ast.Name)), 'Expected argv list (literal or variable) passed to Popen'
