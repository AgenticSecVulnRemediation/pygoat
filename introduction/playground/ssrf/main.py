import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate the 'file' parameter to prevent directory traversal
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path provided')
        normalized_path = os.path.normpath(file)
        if normalized_path.startswith('..'):
            raise ValueError('Invalid file path provided')
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
