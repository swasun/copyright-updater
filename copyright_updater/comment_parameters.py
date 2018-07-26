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

from .simple__repr__ import simple__repr__
from .comment_type import CommentType

class CommentParameters(object):

    def __init__(self, comment_type, symbol, additional_spaces_before_begin_symbol=1, additional_spaces_after_begin_symbol=1,
        additional_spaces_before_end_symbol=2):
        
        self.comment_type = comment_type
        self.symbol = symbol
        self.additional_spaces_before_begin_symbol = additional_spaces_before_begin_symbol
        self.additional_spaces_after_begin_symbol = additional_spaces_after_begin_symbol
        self.additional_spaces_before_end_symbol = additional_spaces_before_end_symbol

    @staticmethod
    def create_from_file_extension(extension, surround=False):
        if extension in ('.py', '.txt', '.cmake'):
            return CommentParameters(CommentType.SURROUND_BY_SYMBOL_NUMBERS if surround else CommentType.SYMBOL_NUMBER, '#')
        elif extension in ('.c', '.h'):
            return CommentParameters(CommentType.SURROUND_BY_STARS if surround else CommentType.SLASH, '*' if surround else '//')
        
        raise ValueError("Unsupported extension file '" + extension + "'")

    def __repr__(self):
        return simple__repr__(self)