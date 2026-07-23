import os


def ssrf_lab(filepath):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(filepath) or '..' in os.path.normpath(filepath):
            raise ValueError('Invalid file path provided')
        filename = os.path.join(dirname, filepath)
        resolved_path = os.path.abspath(filename)
        if os.path.commonpath([os.path.abspath(dirname), resolved_path]) != os.path.abspath(dirname):
            raise ValueError('File path traversal detected')
        with open(resolved_path, "r") as f:
            data = f.read()
        return {"blog":data}
    except (OSError, ValueError):
        return {"blog": "No blog found"}
