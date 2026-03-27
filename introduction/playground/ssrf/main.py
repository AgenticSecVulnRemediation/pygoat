import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate input to prevent path traversal
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path provided')
        # Safely join and normalize the path
        filename = os.path.normpath(os.path.join(dirname, file))
        abs_dir = os.path.abspath(dirname)
        abs_file = os.path.abspath(filename)
        if not abs_file.startswith(abs_dir):
            raise ValueError('File path escapes base directory')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
