import os


def ssrf_lab(file):
    try:
        # Validate the user-supplied file name to prevent path traversal
        if os.path.isabs(file) or '..' in file:
            # TODO: Replace the placeholder error handling as appropriate
            return {"blog": "Invalid file path provided."}
        
        # Compute the full file path and ensure it resides in the intended directory
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        if os.path.commonprefix([os.path.realpath(filename), os.path.realpath(dirname)]) != os.path.realpath(dirname):
            return {"blog": "Invalid file path provided."}
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
