import os


def ssrf_lab(file):
    # Validate 'file' input to ensure it is not an absolute path and does not contain directory traversal sequences
    if os.path.isabs(file) or '..' in file:
        return {"blog": "Invalid file path detected"}
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
