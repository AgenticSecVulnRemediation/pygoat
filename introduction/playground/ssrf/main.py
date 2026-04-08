import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        # Validate the file path to prevent path traversal. Adjust error handling if needed.
        abs_filename = os.path.realpath(filename)
        abs_dir = os.path.realpath(dirname) + os.sep
        if not abs_filename.startswith(abs_dir):
            raise ValueError('Potential path traversal attempt detected')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
