import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        # Validate resolved file path to prevent path traversal
        real_path = os.path.realpath(filename)
        base_dir = os.path.realpath(dirname) + os.sep
        if not real_path.startswith(base_dir):
            raise Exception('Invalid file path: Path traversal attempt detected')
        file = open(real_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
