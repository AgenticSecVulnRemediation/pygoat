import os


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        # Validate that the input 'file' does not contain directory traversal sequences
        if os.path.isabs(file) or '..' in file:
            raise ValueError('Invalid file path supplied')

        # Construct the full path and normalize it
        base_dir = os.path.abspath(os.path.dirname(__file__))
        joined_path = os.path.abspath(os.path.join(base_dir, file))

        # Ensure the resulting path is within the expected directory
        if not joined_path.startswith(base_dir + os.sep):
            raise ValueError('File path escapes allowed directory')

        # Now open the file safely
        with open(joined_path, 'r') as f:
            data = f.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
