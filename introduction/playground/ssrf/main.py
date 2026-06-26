import os


def ssrf_lab(file):
    try:
        base_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(base_dir, file)
        real_target_path = os.path.realpath(filename)
        if not real_target_path.startswith(base_dir + os.sep):
            raise Exception('Invalid file path: Access outside allowed directory')
        file = open(real_target_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
