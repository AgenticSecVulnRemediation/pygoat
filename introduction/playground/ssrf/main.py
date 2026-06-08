import os


def ssrf_lab(file):
    try:
        allowed_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.abspath(os.path.join(allowed_dir, file))
        if not file_path.startswith(allowed_dir + os.sep):
            return {"blog": "Invalid file path"}
        file = open(file_path, "r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
