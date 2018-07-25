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

def uncomment_copyright(copyright):
    uncommented_lines = list()
    begin_index = 0
    last_index = len(copyright.lines)
    additional_end_spaces_to_remove = None
    additional_new_line = ''

    if copyright.comment_parameters.comment_type in (CommentType.SURROUND_BY_SYMBOL_NUMBERS, CommentType.SURROUND_BY_STARS):
        begin_index += 1
        last_index -= 1
        additional_end_spaces_to_remove = -(copyright.comment_parameters.additional_spaces_before_end_symbol + len(copyright.comment_parameters.symbol) + 1)
        additional_new_line = '\n'

    for i in range(begin_index, last_index):
        line = copyright.lines[i]
        uncommented_line = line[copyright.comment_parameters.additional_spaces_before_begin_symbol +
            len(copyright.comment_parameters.symbol) + copyright.comment_parameters.additional_spaces_after_begin_symbol:
            additional_end_spaces_to_remove].rstrip(' ')
        uncommented_lines.append(uncommented_line + additional_new_line)

    uncommented_copyright = Copyright(uncommented_lines, copyright.comment_parameters)

    return uncommented_copyright
