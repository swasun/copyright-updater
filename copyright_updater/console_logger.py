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

from .color_print import ColorPrint

import sys
import traceback

class ConsoleLogger(object):

    @staticmethod
    def status(message):
        ColorPrint.print_info('[~] {message}'.format(message=message))

    @staticmethod
    def success(message):
        ColorPrint.print_pass('[+] {message}'.format(message=message))

    @staticmethod
    def error(message):
        if (sys.exc_info()[2]):
            line = traceback.extract_tb(sys.exc_info()[2])[-1].lineno
            error_message = '[-] {message} with cause: {cause} (line {line})'.format( \
                message=message, cause=str(sys.exc_info()[1]), line=line)
        else:
            error_message = '[-] {message}'.format(message=message)
        ColorPrint.print_fail(error_message)
        
    @staticmethod
    def warn(message):
        ColorPrint.print_warn('[-] {message}'.format(message=message))