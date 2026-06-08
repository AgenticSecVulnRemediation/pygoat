import os


def ssrf_lab(file):
    if os.path.isabs(file) or '..' in file:
        # TODO: Replace with your error handling mechanism, e.g., logging or raising a specific exception
        raise ValueError('Invalid file path provided.')
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
