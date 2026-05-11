import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate the file parameter to prevent path traversal
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path')
        # Validate the file parameter to prevent path traversal
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path')
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
