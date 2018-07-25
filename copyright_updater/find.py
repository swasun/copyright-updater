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

from .comment_type import CommentType
from .comment_parameters import CommentParameters
from .copyright import Copyright

def is_copyright_exist(file_name):
    with open(file_name, 'r') as f:
        file_lines = f.readlines()
    try:
        find_copyright(file_lines)
    except:
        return False
    return True

def find_copyright(file_lines):
    file_lines_len = len(file_lines)
    copyright = None
    copyright_index = -1
    first_commented_line_index = -1
    last_commented_line_index = -1
    comment_type = CommentType.UNKNOWN
    symbol = None
    additional_spaces_before_begin_symbol = 1
    additional_spaces_after_begin_symbol = 1
    additional_spaces_before_end_symbol = 2
    comment_parameters = None

    # Find the Copyright string location
    for i in range(0, file_lines_len):
        line = file_lines[i]
        if 'Copyright' in line or 'copyright' in line:
            copyright_index = i
            break

    # Leave if the Copyright string wasn't found
    if copyright_index == -1:
        raise ValueError('Failed to find copyright index')

    # Find the first commented line and the comment type of the copyright
    if copyright_index == 0:
        first_commented_line_index = 0
        if file_lines[first_commented_line_index].lstrip(' ').startswith('#'):
            comment_type = CommentType.SYMBOL_NUMBER
            symbol = '#'
        elif file_lines[first_commented_line_index].lstrip(' ').startswith('//'):
            comment_type = CommentType.SLASH
            symbol = '//'
    else:
        for i in range(copyright_index, -1, -1):
            line = file_lines[i]
            if line.lstrip(' ').startswith('/*'):
                comment_type = CommentType.SURROUND_BY_STARS
                symbol = '*'
                break
            elif line.lstrip(' ').startswith('###'):
                comment_type = CommentType.SURROUND_BY_SYMBOL_NUMBERS
                symbol = '#'
                first_commented_line_index = i
                break

    # Leave if the copyright type wasn't recognized
    if comment_type == CommentType.UNKNOWN:
        raise ValueError("Failed to recognized comment type")

    # Find the last commented line of the copyright
    if comment_type == CommentType.SURROUND_BY_STARS:
        for i in range(first_commented_line_index, file_lines_len):
            line = file_lines[i]
            if line.rstrip().endswith('*/'):
                last_commented_line_index = i+1
                break
    elif comment_type == CommentType.SURROUND_BY_SYMBOL_NUMBERS:
        symbol_numbers_line = file_lines[first_commented_line_index].replace('\n', '')
        for i in range(first_commented_line_index+1, file_lines_len):
            if file_lines[i] in (symbol_numbers_line, symbol_numbers_line + '\n'):
                last_commented_line_index = i+1
                break
    elif comment_type == CommentType.SYMBOL_NUMBER:
        for i in range(first_commented_line_index, file_lines_len):
            if not file_lines[i].lstrip(' ').startswith('#'):
                last_commented_line_index = i
                break
    elif comment_type == CommentType.SLASH:
        for i in range(first_commented_line_index, file_lines_len):
            if not file_lines[i].lstrip(' ').startswith('//'):
                last_commented_line_index = i
                break

    # Leave if the last commented line of the copyright wasn't found
    if last_commented_line_index == -1:
        raise ValueError("Failed to find the last commented line of copyright")

    # Get the number of spaces before the comment symbol
    additional_spaces_before_begin_symbol = len(file_lines[copyright_index]) - len(file_lines[copyright_index].lstrip(' '))
    if additional_spaces_before_begin_symbol < 0:
        raise ValueError("Failed to fidn the additional spaces before begin symbol")

    copyright_lines = file_lines[first_commented_line_index:last_commented_line_index]

    left_strip_copyright_line = file_lines[copyright_index].lstrip(' ')
    additional_spaces_after_begin_symbol = len(left_strip_copyright_line) - len(left_strip_copyright_line[len(symbol):])

    if comment_type in (CommentType.SURROUND_BY_STARS, CommentType.SURROUND_BY_SYMBOL_NUMBERS):
        additionals_spaces_before_end_symbol = list()
        for line in copyright_lines:
            additionals_spaces_before_end_symbol.append(len(line) + len(symbol) - len(line[:-len(symbol)].rstrip(' ')))
        additional_spaces_before_end_symbol = min(additionals_spaces_before_end_symbol)

    comment_parameters = CommentParameters(comment_type, symbol, additional_spaces_before_begin_symbol,
        additional_spaces_after_begin_symbol, additional_spaces_before_end_symbol)

    copyright = Copyright(copyright_lines, comment_parameters)

    return copyright