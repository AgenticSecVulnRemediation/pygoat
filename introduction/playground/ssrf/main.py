import os


def ssrf_lab(file):
    # Validate file input to disallow absolute paths or directory traversal sequences
    if os.path.isabs(file) or '..' in file:
        return {"blog": "Invalid file path."}
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except (IOError, FileNotFoundError):
        return {"blog": "No blog found"}
