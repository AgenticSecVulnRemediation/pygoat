import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Normalize the file input to prevent directory traversal
        normalized_file = os.path.normpath(file)
        # Check for directory traversal or absolute paths
        if os.path.isabs(normalized_file) or normalized_file.startswith('..') or '..' in normalized_file.split(os.sep):
            raise ValueError('Invalid file path')
        filename = os.path.join(dirname, normalized_file)
        # Resolve the absolute path and ensure it is within the allowed directory
        abs_filename = os.path.abspath(filename)
        allowed_dir = os.path.abspath(dirname)
        if not abs_filename.startswith(allowed_dir):
            raise ValueError('Access to specified file is not allowed')
        with open(abs_filename, "r") as f:
            data = f.read()
            return {"blog": data}
    except ValueError as e:
        return {"blog": str(e)}
    except Exception:
        return {"blog": "No blog found"}
