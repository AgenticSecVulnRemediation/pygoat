import os


def ssrf_lab(file):
    # Validate the file input to prevent path traversal
    if os.path.isabs(file) or '..' in file:
        raise ValueError('Invalid file input: Absolute paths or directory traversal not allowed')
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
