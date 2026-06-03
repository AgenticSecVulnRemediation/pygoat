import os


def ssrf_lab(file):
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        normalized_file = os.path.normpath(file)
        if os.path.isabs(normalized_file):
            raise ValueError('Absolute paths not allowed')
        file_path = os.path.join(base_dir, normalized_file)
        if os.path.commonpath([base_dir, os.path.abspath(file_path)]) != base_dir:
            raise ValueError('Attempted directory traversal detected')
        file = open(file_path, "r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
