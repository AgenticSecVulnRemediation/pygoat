import os


def ssrf_lab(file):
    try:
        # Validate the file parameter to prevent directory traversal
        if os.path.isabs(file) or '..' in os.path.normpath(file):
            raise ValueError('Invalid file path provided.')
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except Exception:
        return {"blog": "No blog found"}
