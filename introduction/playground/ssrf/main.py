import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate the user-supplied file input to prevent directory traversal
        # This validation ensures that any file path containing directory traversal sequences
        # or being absolute is immediately rejected, preventing unauthorized filesystem access
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path provided')

        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
