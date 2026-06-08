import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            return {"blog": "Invalid file path provided"}
        full_path = os.path.abspath(os.path.join(dirname, file))
        if not full_path.startswith(os.path.abspath(dirname)):
            return {"blog": "Invalid file path provided"}
        file = open(full_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
