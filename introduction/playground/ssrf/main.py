import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        file_norm = os.path.normpath(file)
        if os.path.isabs(file_norm) or file_norm.startswith('..') or '..' in file_norm.split(os.sep):
            return {"blog": "Invalid file path."}
        filename = os.path.join(dirname, file_norm)
        if not os.path.abspath(filename).startswith(os.path.abspath(dirname) + os.sep):
            return {"blog": "Invalid file path."}
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
