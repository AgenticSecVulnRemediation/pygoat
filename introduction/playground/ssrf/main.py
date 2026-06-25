import os


def ssrf_lab(file):
    try:
        if os.path.isabs(file) or '..' in file:
            # TODO: Replace with an appropriate error message or handling mechanism
            raise ValueError('Invalid file path')
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        # Validate that the resolved path remains within the expected directory
        if not os.path.realpath(filename).startswith(os.path.realpath(dirname)):
            # TODO: Replace with an appropriate error message or handling mechanism
            raise ValueError('Unauthorized file access')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
