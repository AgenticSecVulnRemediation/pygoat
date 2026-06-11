import os


def ssrf_lab(file):
    try:
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path provided')  # TODO: Customize error handling as needed
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except ValueError as ve:
        return {"blog": f"Invalid file path provided: {ve}"}
    except Exception:
        return {"blog": "No blog found"}
        return {"blog": "No blog found"}
