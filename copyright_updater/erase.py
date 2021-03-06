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

from .console_logger import ConsoleLogger
from .copyright import Copyright
from .comment_parameters import CommentParameters
from .comment import comment_copyright
from .find import find_copyright, is_copyright_exist

from shutil import copyfile
import os

def erase_copyright(target_file_name, with_backup):
    with open(target_file_name, 'r') as f:
        file_lines = f.readlines()
    try:
        copyright = find_copyright(file_lines)
    except:
        ConsoleLogger.status('No copyright detected in ' + target_file_name + ' - skipping.')
        return True
    
    with open(target_file_name, 'r') as target_file:
        target_content = target_file.read()
    if with_backup:
        copyfile(target_file_name, target_file_name + '.backup')
    os.remove(target_file_name)
    with open(target_file_name, 'w') as new_file:
        copyright_content = ''.join(copyright.lines)
        new_content = target_content.replace(copyright_content + '\n' + '\n', '')
        new_content = new_content.replace(copyright_content + '\n', '')
        new_content = new_content.replace(copyright_content, '')
        new_file.write(new_content)
    ConsoleLogger.success('Copyright erased in ' + target_file_name)
    return True