import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate that the filename is not an absolute path and does not contain directory traversal
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path: directory traversal detected')
        # Validate that the filename is not an absolute path and does not contain directory traversal
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path: directory traversal detected')
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
