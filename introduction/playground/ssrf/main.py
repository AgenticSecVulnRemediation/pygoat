import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Construct the absolute candidate path
        candidate = os.path.abspath(os.path.join(dirname, file))
        # Validate candidate is within the base directory to prevent directory traversal
        if os.path.commonpath([dirname, candidate]) != os.path.abspath(dirname):
            # Optionally log the error or raise an exception
            raise Exception('Invalid file path: directory traversal attempt detected')
        file = open(candidate, 'r')
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
