import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        joined_path = os.path.join(dirname, file)
        filename = os.path.realpath(joined_path)  # Normalize the path
        if not filename.startswith(os.path.realpath(dirname) + os.sep):
            raise Exception('Unauthorized file path')  # Prevent path traversal
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
