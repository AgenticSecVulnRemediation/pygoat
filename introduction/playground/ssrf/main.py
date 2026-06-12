import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        base_directory = os.path.realpath(dirname)
        joined_path = os.path.join(base_directory, file)
        resolved_path = os.path.realpath(joined_path)
        if not resolved_path.startswith(base_directory + os.sep):
            raise ValueError('Invalid file path')
        file = open(resolved_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
