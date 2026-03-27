import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if os.path.isabs(file):
            raise ValueError('Absolute paths are not allowed')
        if '..' in file:
            raise ValueError('Directory traversal sequences are not allowed')
        base_dir = os.path.realpath(dirname)
        full_path = os.path.realpath(os.path.join(base_dir, file))
        if not full_path.startswith(base_dir + os.sep):
            raise ValueError('Resolved path is outside the allowed directory')
        filename = full_path
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
