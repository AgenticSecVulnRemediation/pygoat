import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path provided')
        safe_file = os.path.normpath(file)
        full_path = os.path.join(dirname, safe_file)
        if not full_path.startswith(dirname + os.sep):
            raise ValueError('File path escapes the allowed directory')
        file = open(full_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
