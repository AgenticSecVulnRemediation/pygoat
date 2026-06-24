import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path provided')
        filename = os.path.join(dirname, file)
        if not os.path.realpath(filename).startswith(os.path.realpath(dirname)):
            raise ValueError('Invalid file path: outside allowed directory')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
