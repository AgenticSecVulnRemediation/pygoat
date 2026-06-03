import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        if '..' in file or os.path.isabs(file):
            # TODO: Replace the exception message as appropriate for your application
            raise ValueError('Invalid file path provided.')
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
