import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path provided')

        # Build and normalize file path
        filename = os.path.join(dirname, file)
        normalized_filename = os.path.normpath(filename)
        if not normalized_filename.startswith(os.path.abspath(dirname)):
            raise ValueError('Attempted Directory Traversal')
        with open(normalized_filename, "r") as f:
            data = f.read()
        return {"blog": data}
    except:
        return {"blog": "No blog found"}
