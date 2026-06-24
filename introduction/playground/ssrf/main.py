import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if '..' in file or os.path.isabs(file):
            return {"blog": "Invalid file path."}
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
