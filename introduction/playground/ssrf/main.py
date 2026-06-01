import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate the input file path to prevent directory traversal
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path provided')
        normalized_file = os.path.normpath(file)
        if normalized_file.startswith('..'):
            raise ValueError('Invalid file path provided')
        filename = os.path.join(dirname, normalized_file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
