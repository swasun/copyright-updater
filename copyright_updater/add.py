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

def add_copyright(target_file_name, copyright_lines, with_backup, with_surround):
    if is_copyright_exist(target_file_name):
        ConsoleLogger.warn("A copyright already exists in " + target_file_name)
        return False
    with open(target_file_name, 'r') as target_file:
        target_content = target_file.read()
    if with_backup:
        copyfile(target_file_name, target_file_name + '.backup')
    os.remove(target_file_name)
    copyright = Copyright(copyright_lines, CommentParameters.create_from_file_extension(os.path.splitext(target_file_name)[1], with_surround))
    commented_copyright = comment_copyright(copyright)
    copyright_content = ''.join(commented_copyright.lines)
    with open(target_file_name, 'w') as new_file:
        new_file.write(copyright_content + '\n' + target_content)
    ConsoleLogger.success('Copyright added in ' + target_file_name)
    return True