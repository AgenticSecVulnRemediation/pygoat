import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate the file input to prevent directory traversal
        if os.path.isabs(file) or '..' in file:
            return {"blog": "Invalid file input"}
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
