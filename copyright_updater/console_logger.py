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