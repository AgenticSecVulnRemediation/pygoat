import os


def ssrf_lab(file):
    try:
        base_dir = os.path.realpath(os.path.dirname(__file__))
        canonical_path = os.path.realpath(os.path.join(base_dir, file))
        if not canonical_path.startswith(base_dir):
            raise Exception('Access to files outside the designated directory is not allowed')
        file = open(canonical_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
