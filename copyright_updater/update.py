from .comment import comment_copyright
from .uncomment import uncomment_copyright
from .copyright import Copyright
from .find import find_copyright
from .utils import chunkify, list_target_files, read_lines

import os
from concurrent import futures

def update_copyright_date(copyright, previous_date, new_date):
    for i in range(0, len(copyright.lines)):
        line = copyright.lines[i]
        if 'Copyright' in line or 'copyright' in line:
            if previous_date in line:
                copyright.lines[i] = line.replace(previous_date, new_date)
                return True
            return False
    return False

def update_copyright_author(copyright, previous_author, new_author):
    for i in range(0, len(copyright.lines)):
        line = copyright.lines[i]
        if 'Copyright' in line or 'copyright' in line:
            if previous_author in line:
                copyright.lines[i] = line.replace(previous_author, new_author)
                return True
            return False
    return False

def update_copyright_project_name(copyright, previous_project_name, new_project_name):
    for i in range(0, len(copyright.lines)):
        line = copyright.lines[i]
        if previous_project_name in line:
            copyright.lines[i] = line.replace(previous_project_name, new_project_name)

def test():
    file_name = 'tests/example.c'

    with open(file_name, 'r') as f:
        file_lines = f.readlines()
    
    copyright = find_copyright(file_lines)

    print(''.join(copyright.lines))

    uncommented_copyright = uncomment_copyright(copyright)

    print(''.join(uncommented_copyright.lines))

    update_copyright_date(uncommented_copyright, '2018', '2019')
    update_copyright_author(uncommented_copyright, 'Charly Lamothe', 'Swa')
    update_copyright_project_name(uncommented_copyright, 'LibUnknownEchoCryptoModule', 'Wesh')

    print(''.join(uncommented_copyright.lines))

    new_copyright = comment_copyright(uncommented_copyright)

    print(''.join(new_copyright.lines))

