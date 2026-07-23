import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate user input to prevent directory traversal (safe file resolution)
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path provided')
        safe_path = os.path.join(dirname, file)
        resolved_path = os.path.abspath(safe_path)
        if not resolved_path.startswith(os.path.abspath(dirname)):
            raise ValueError('Path traversal attempt detected')
        # Open file using resolved safe path
        file = open(resolved_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
