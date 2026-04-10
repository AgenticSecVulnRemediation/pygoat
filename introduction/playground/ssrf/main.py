import os


def ssrf_lab(file):
    # Validate the user input to prevent path traversal
    if os.path.isabs(file) or '..' in file:
        return {"blog": "Invalid file path provided."}
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
