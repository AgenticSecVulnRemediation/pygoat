import os


def ssrf_lab(file):
    try:
        # Validate input: disallow directory traversal sequences and absolute paths
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path supplied')

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        # Ensure the constructed path is within the allowed directory
        if not os.path.realpath(filename).startswith(os.path.realpath(dirname)):
            raise ValueError('Attempted directory traversal detected')
        file_obj = open(filename, "r")
        data = file_obj.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
