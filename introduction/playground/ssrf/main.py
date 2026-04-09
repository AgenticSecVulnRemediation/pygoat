import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path')
        filename = os.path.join(dirname, file)
        resolved_filename = os.path.abspath(filename)
        if not resolved_filename.startswith(os.path.abspath(dirname)):
            raise ValueError('Path traversal attempt detected')
        filename = resolved_filename
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
