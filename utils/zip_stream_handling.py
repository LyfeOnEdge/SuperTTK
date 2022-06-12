from zipfile import ZipFile


def get_members(zip):
    parts = []
    # get all the path prefixes
    for name in zip.namelist():
        # only check files (not directories)
        if not name.endswith("/"):
            # keep list of path elements (minus filename)
            parts.append(name.split("/")[:-1])
    # now find the common path prefix (if any)
    prefix = os.path.commonprefix(parts)
    if prefix:
        # re-join the path elements
        prefix = "/".join(prefix) + "/"
    # get the length of the common prefix
    offset = len(prefix)
    # now re-set the filenames
    for zipinfo in zip.infolist():
        name = zipinfo.filename
        # only check files (not directories)
        if len(name) > offset:
            # remove the common prefix
            zipinfo.filename = name[offset:]
            yield zipinfo


# Takes a zip file bytream into memory and extracts it
def handleZIP(file, extract_dir):
    print("Extracting...")
    with ZipFile(io.BytesIO(file), "r") as zipObj:
        zipObj.extractall(extract_dir, get_members(zipObj))
        print("Extracted files - {}".format(zipObj.namelist()))
