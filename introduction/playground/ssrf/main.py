import os


def ssrf_lab(file):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.abspath(os.path.join(base_dir, file))
        if not target_path.startswith(base_dir + os.sep):
            raise ValueError('Invalid file path: escaping base directory is not allowed')
        file = open(target_path, "r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
