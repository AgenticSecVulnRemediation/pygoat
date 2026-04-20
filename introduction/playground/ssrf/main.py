import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path: directory traversal detected')
        filename = os.path.join(dirname, file)
        safe_path = os.path.abspath(filename)
        if not safe_path.startswith(os.path.abspath(dirname)):
            raise ValueError('Invalid file path: traversal outside allowed directory')
        file = open(safe_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
