import os
import logging


def ssrf_lab(file):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.realpath(os.path.join(os.path.dirname(__file__), file))
        base_dir = os.path.realpath(os.path.dirname(__file__))
        if not filename.startswith(base_dir + os.sep):
            raise ValueError('Invalid file path')
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except Exception as e:
        logging.error("Error occurred while reading file", exc_info=True)  # Log detailed error. Adjust logging configuration as needed.
        return {"blog": "No blog found"}
