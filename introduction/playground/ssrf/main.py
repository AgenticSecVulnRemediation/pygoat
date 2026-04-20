import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate the file parameter to prevent path traversal
        if '..' in file or os.path.isabs(file):
            raise Exception('Invalid file path input: potential path traversal')
        filename = os.path.abspath(os.path.join(dirname, file))
        if not filename.startswith(os.path.abspath(dirname)):
            raise Exception('Resolved path is outside of allowed directory')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
