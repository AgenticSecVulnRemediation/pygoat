import os


def ssrf_lab(file):
    # Validate file input to prevent CWE-73 (External Control of File Name or Path) vulnerabilities by mitigating directory traversal attacks.
    if os.path.isabs(file) or '..' in file:
        return {"blog": "Invalid file path"}
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, file)
        file = open(filename,"r")
        data = file.read()
        return {"blog":data}
    except:
        return {"blog": "No blog found"}
