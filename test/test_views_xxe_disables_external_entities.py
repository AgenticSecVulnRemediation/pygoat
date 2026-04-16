import ast


def _find_function_def(module_ast: ast.AST, name: str) -> ast.FunctionDef:
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Function {name} not found")


def test_xxe_parse_sets_feature_external_ges_false():
    """Delta: parser.setFeature(feature_external_ges, False)"""
    src = open('introduction/views.py', 'r', encoding='utf-8').read()
    module_ast = ast.parse(src)

    fn = _find_function_def(module_ast, 'xxe_parse')

    setfeature_calls = [
        n for n in ast.walk(fn)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == 'setFeature'
    ]

    assert setfeature_calls, 'Expected setFeature call in xxe_parse'
    # Find call where second arg is False
    assert any(len(c.args) >= 2 and isinstance(c.args[1], ast.Constant) and c.args[1].value is False for c in setfeature_calls)
