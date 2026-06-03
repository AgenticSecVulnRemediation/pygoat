import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate input file to prevent path traversal attacks
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path - absolute paths or directory traversal sequences are not allowed')
        safe_path = os.path.normpath(os.path.join(dirname, file))
        if not safe_path.startswith(os.path.abspath(dirname)):
            raise ValueError('Invalid file path - attempted directory escape')
        filename = safe_path
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
