import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        abs_filename = os.path.abspath(os.path.join(dirname, file))
        base_dir = os.path.abspath(dirname)
        if os.path.commonpath([abs_filename, base_dir]) != base_dir:
            raise Exception('Invalid file path: potential path traversal attempt.')
        file = open(abs_filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
