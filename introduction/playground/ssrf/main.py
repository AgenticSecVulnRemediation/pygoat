import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        normalized_file = os.path.normpath(file)
        abs_file_path = os.path.abspath(os.path.join(dirname, normalized_file))
        if os.path.commonpath([abs_file_path, os.path.abspath(dirname)]) != os.path.abspath(dirname):
            raise ValueError('Invalid file path')
        with open(abs_file_path, "r") as f:
            data = f.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
