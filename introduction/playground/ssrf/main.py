import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        canonical_path = os.path.abspath(filename)
        base_dir = os.path.abspath(dirname)
        if not canonical_path.startswith(base_dir + os.sep):
            raise Exception('Invalid file path: potential path traversal attempt detected')
        file = open(canonical_path, "r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
