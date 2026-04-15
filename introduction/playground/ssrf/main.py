import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate input to prevent path traversal
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file parameter: potential path traversal detected')
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
