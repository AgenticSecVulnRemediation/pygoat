import os


def ssrf_lab(file):
    try:
        base_dir = os.path.dirname(__file__)
        full_path = os.path.join(base_dir, file)
        norm_path = os.path.normpath(full_path)
        # Ensure norm_path is within the trusted directory
        if not os.path.abspath(norm_path).startswith(os.path.abspath(base_dir)):
            # TODO: Replace with appropriate error handling for invalid file paths
            return {"blog": "Invalid file path."}
        file = open(norm_path, "r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
