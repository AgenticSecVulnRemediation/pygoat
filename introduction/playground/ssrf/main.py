import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate input: reject absolute paths and directory traversal sequences
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file name provided')
        fullname = os.path.join(dirname, file)
        fullname = os.path.realpath(fullname)
        # Ensure the resolved path is within the allowed directory
        if not fullname.startswith(os.path.realpath(dirname) + os.sep):
            raise ValueError('Invalid file path provided')
        with open(fullname, "r") as f:
            data = f.read()
        return {"blog": data}
    except Exception as e:
        return {"blog": "No blog found"}
