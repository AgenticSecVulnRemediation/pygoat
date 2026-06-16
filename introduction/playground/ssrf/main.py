import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate that the file parameter does not contain directory traversal sequences or absolute paths
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path parameter')
        # Validate that the file parameter does not contain directory traversal sequences or absolute paths
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path parameter')
        # Validate that the file parameter does not contain directory traversal sequences or absolute paths
        if '..' in file or os.path.isabs(file):
            raise ValueError('Invalid file path parameter')
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
