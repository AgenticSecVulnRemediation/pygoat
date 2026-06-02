import os


def ssrf_lab(file):
    try:
        dirname = os.path.abspath(os.path.dirname(__file__))
        if os.path.isabs(file) or '..' in file:
            raise ValueError("Invalid file path provided")
        safe_path = os.path.abspath(os.path.join(dirname, file))
        if not safe_path.startswith(dirname):
            raise ValueError("Invalid file path provided")
        file_handle = open(safe_path,"r")
        data = file_handle.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
