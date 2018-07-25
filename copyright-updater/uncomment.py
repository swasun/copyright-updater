

from comment_type import CommentType
from comment_parameters import CommentParameters
from copyright import Copyright

def uncomment_copyright(copyright):
    uncommented_lines = list()
    begin_index = 0
    last_index = len(copyright.lines)
    additional_end_spaces_to_remove = None
    additional_new_line = ''

    if copyright.comment_parameters.comment_type in (CommentType.SUROUND_BY_SYMBOL_NUMBERS, CommentType.SUROUND_BY_STARS):
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
