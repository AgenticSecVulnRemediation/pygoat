import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(os.path.realpath(__file__))
        full_path = os.path.join(dirname, file)
        real_path = os.path.realpath(full_path)
        if not real_path.startswith(os.path.join(os.path.dirname(os.path.realpath(__file__)), '')):
            raise Exception('Invalid file path')
        file = open(real_path,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
