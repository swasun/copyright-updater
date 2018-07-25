import os

def chunkify(lst, n):
    """ Inspired from https://stackoverflow.com/a/2136090
    """
    return [lst[i::n] for i in range(n)]

def read_lines(file_name):
    with open(file_name, 'r') as copyright_file:
        return [line.rstrip() for line in copyright_file.read().splitlines()]

def list_target_files(root_dir):
    target_files = list()
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            target_files.append(subdir + os.sep + file)
    return target_files