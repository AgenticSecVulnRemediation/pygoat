import os


def ssrf_lab(file):
    try:
        # Validate against directory traversal and absolute path
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path provided')
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
