import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.normpath(os.path.join(dirname, file))
        if not filename.startswith(dirname):
            # The normalized path escapes the intended directory
            raise ValueError('Invalid file path input')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
