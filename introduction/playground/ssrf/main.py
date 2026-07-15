import os


def ssrf_lab(file):
    try:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(base_dir, file)
        normalized_path = os.path.realpath(filename)
        if os.path.commonpath([base_dir, normalized_path]) != base_dir:
            raise ValueError('Invalid file path: directory traversal detected')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
