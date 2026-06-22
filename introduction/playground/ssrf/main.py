import os


def ssrf_lab(file):
    if '..' in file or os.path.isabs(file):
        # Check prevents path traversal by disallowing directory escape sequences and absolute paths.
        raise ValueError('Invalid file parameter')
    try:
        if '..' in file or os.path.isabs(file):
            # This check prevents path traversal by disallowing directory escape sequences and absolute paths.
            raise ValueError('Invalid file parameter')
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
