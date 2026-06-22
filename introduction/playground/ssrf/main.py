import os


def ssrf_lab(file):
    try:
        if os.path.isabs(file) or '..' in os.path.normpath(file):
            raise ValueError('Invalid file path')
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
