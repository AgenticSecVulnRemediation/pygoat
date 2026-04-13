import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            raise ValueError("Invalid file path")
        filename = os.path.join(dirname, file)
        abs_base = os.path.abspath(dirname)
        abs_path = os.path.abspath(filename)
        if not abs_path.startswith(abs_base + os.sep):
            raise ValueError("Invalid file path")
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
