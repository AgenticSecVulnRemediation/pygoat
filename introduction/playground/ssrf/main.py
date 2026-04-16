import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            return {"blog": "Invalid file path: Access denied."}
        filename = os.path.join(dirname, file)
        filename = os.path.normpath(filename)
        if not filename.startswith(dirname):
            return {"blog": "Invalid file path: Directory traversal detected."}
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
