 #####################################################################################
 # MIT License                                                                       #
 #                                                                                   #
 # Copyright (C) 2018 Charly Lamothe                                                 #
 #                                                                                   #
 # This file is part of copyright-updater.                                           #
 #                                                                                   #
 #   Permission is hereby granted, free of charge, to any person obtaining a copy    #
 #   of this software and associated documentation files (the "Software"), to deal   #
 #   in the Software without restriction, including without limitation the rights    #
 #   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       #
 #   copies of the Software, and to permit persons to whom the Software is           #
 #   furnished to do so, subject to the following conditions:                        #
 #                                                                                   #
 #   The above copyright notice and this permission notice shall be included in all  #
 #   copies or substantial portions of the Software.                                 #
 #                                                                                   #
 #   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
 #   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        #
 #   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     #
 #   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          #
 #   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   #
 #   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   #
 #   SOFTWARE.                                                                       #
 #####################################################################################

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

