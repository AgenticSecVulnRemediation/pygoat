import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Normalize the user-supplied file path
        safe_file = os.path.normpath(file)
        # Reject absolute paths or paths with directory traversal
        if os.path.isabs(safe_file) or '..' in safe_file.split(os.sep):
            raise ValueError('Invalid file path provided')
        filename = os.path.join(dirname, safe_file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
