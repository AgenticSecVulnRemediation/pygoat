import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            return {"blog": "Invalid file path provided"}
        filename = os.path.join(dirname, file)
        normalized_path = os.path.realpath(filename)
        if not normalized_path.startswith(os.path.realpath(dirname) + os.sep):
            return {"blog": "Invalid file path provided"}
        filename = normalized_path
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
