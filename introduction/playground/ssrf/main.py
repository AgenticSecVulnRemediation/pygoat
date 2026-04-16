import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        # Resolve the real path and check if it starts with the expected directory
        real_filename = os.path.realpath(filename)
        if not real_filename.startswith(os.path.realpath(dirname) + os.sep):
            raise Exception('Invalid path: directory traversal detected')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
