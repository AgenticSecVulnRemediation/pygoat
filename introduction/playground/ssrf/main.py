import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate the file name
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file name: directory traversal detected')
        filename = os.path.join(dirname, file)
        # Ensure the resolved path is within the expected directory
        abs_path = os.path.abspath(filename)
        if not abs_path.startswith(os.path.abspath(dirname) + os.sep):
            raise ValueError('Resolved path is outside the permitted directory')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
