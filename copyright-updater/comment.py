from utils import read_lines
from comment_type import CommentType
from copyright import Copyright

def _suround_with_symbol(copyright_lines, symbol, max_length, additional_spaces_before_begin_symbol, additional_spaces_after_begin_symbol,
    additional_spaces_before_end_symbol):

    commented_copyright_lines = list()

    for line in copyright_lines:
        line = line.replace('\n', '')

        if len(line) != max_length:
            missing_spaces = ' ' * (max_length - len(line))
            line = line + missing_spaces

        new_line = (' ' * additional_spaces_before_begin_symbol) + \
            symbol + \
            (' ' * additional_spaces_after_begin_symbol) + \
            line + \
            (' ' * additional_spaces_before_end_symbol) + \
            symbol + \
            '\n'
        commented_copyright_lines.append(new_line)

    return commented_copyright_lines

def _comment_with_symbol(copyright_lines, symbol, max_length, additional_spaces_before_begin_symbol, additional_spaces_after_begin_symbol,
    additional_spaces_before_end_symbol):

    commented_copyright_lines = list()

    for line in copyright_lines:
        if len(line) != max_length:
            missing_spaces = ' ' * (max_length - len(line))
            line = line + missing_spaces

        new_line = (' ' * additional_spaces_before_begin_symbol) + \
            symbol + \
            (' ' * additional_spaces_after_begin_symbol) + \
            line + \
            (' ' * additional_spaces_before_end_symbol) + \
            '\n'
        commented_copyright_lines.append(new_line)

    commented_copyright_lines[-1] = commented_copyright_lines[-1].replace('\n', '')

    return commented_copyright_lines

def suround_with_stars(copyright_lines, additional_spaces_before_begin_symbol=1, additional_spaces_after_begin_symbol=1,
    additional_spaces_before_end_symbol=2):

    max_length, _ = max([(len(x), x) for x in copyright_lines])
    commented_copyright_lines = _suround_with_symbol(copyright_lines, '*', max_length, additional_spaces_before_begin_symbol,
        additional_spaces_after_begin_symbol, additional_spaces_before_end_symbol)

    star_line = ('*' * (max_length + additional_spaces_before_begin_symbol + additional_spaces_after_begin_symbol + additional_spaces_before_end_symbol + 1))
    commented_copyright_lines = ['/' + star_line + '\n'] + commented_copyright_lines + [(' ' * additional_spaces_before_begin_symbol) + star_line + '/']

    return commented_copyright_lines

def suround_with_number_symbols(copyright_lines, additional_spaces_before_begin_symbol=1, additional_spaces_after_begin_symbol=1,
    additional_spaces_before_end_symbol=2):

    max_length, _ = max([(len(x), x) for x in copyright_lines])
    commented_copyright_lines = _suround_with_symbol(copyright_lines, '#', max_length, additional_spaces_before_begin_symbol,
        additional_spaces_after_begin_symbol, additional_spaces_before_end_symbol)

    star_line = ('#' * (max_length + additional_spaces_before_begin_symbol + additional_spaces_after_begin_symbol + additional_spaces_before_end_symbol + 1))
    commented_copyright_lines = [(' ' * additional_spaces_before_begin_symbol) + star_line + '\n'] + commented_copyright_lines + [(' ' * additional_spaces_before_begin_symbol) + star_line]

    return commented_copyright_lines

def comment_with_slash(copyright_lines, additional_spaces_before_begin_symbol=1, additional_spaces_after_begin_symbol=1,
    additional_spaces_before_end_symbol=2):

    max_length, _ = max([(len(x), x) for x in copyright_lines])
    commented_copyright_lines = _comment_with_symbol(copyright_lines, '/', max_length, additional_spaces_before_begin_symbol,
        additional_spaces_after_begin_symbol, additional_spaces_before_end_symbol)

    return commented_copyright_lines

def comment_with_symbol_numbers(copyright_lines, additional_spaces_before_begin_symbol=1, additional_spaces_after_begin_symbol=1,
    additional_spaces_before_end_symbol=2):

    max_length, _ = max([(len(x), x) for x in copyright_lines])
    commented_copyright_lines = _comment_with_symbol(copyright_lines, '#', max_length, additional_spaces_before_begin_symbol,
        additional_spaces_after_begin_symbol, additional_spaces_before_end_symbol)

    return commented_copyright_lines

def comment_copyright(copyright):
    if copyright.comment_parameters.comment_type is CommentType.SUROUND_BY_STARS:
        lines = suround_with_stars(copyright.lines, copyright.comment_parameters.additional_spaces_before_begin_symbol,
            copyright.comment_parameters.additional_spaces_after_begin_symbol, copyright.comment_parameters.additional_spaces_before_end_symbol) + ['\n']
    elif copyright.comment_parameters.comment_type is CommentType.SUROUND_BY_SYMBOL_NUMBERS:
        lines = suround_with_number_symbols(copyright.lines, copyright.comment_parameters.additional_spaces_before_begin_symbol,
            copyright.comment_parameters.additional_spaces_after_begin_symbol, copyright.comment_parameters.additional_spaces_before_end_symbol) + ['\n']
    elif copyright.comment_parameters.comment_type is CommentType.SLASH:
        lines = comment_with_slash(copyright.lines, copyright.comment_parameters.additional_spaces_before_begin_symbol,
            copyright.comment_parameters.additional_spaces_after_begin_symbol, copyright.comment_parameters.additional_spaces_before_end_symbol) + ['\n']
    elif copyright.comment_parameters.comment_type is CommentType.SYMBOL_NUMBER:
        lines = comment_with_symbol_numbers(copyright.lines, copyright.comment_parameters.additional_spaces_before_begin_symbol,
            copyright.comment_parameters.additional_spaces_after_begin_symbol, copyright.comment_parameters.additional_spaces_before_end_symbol) + ['\n']
    else:
        raise ValueError('Unsupported comment type')

    return Copyright(lines, copyright.comment_parameters)

def test_comments():
    copyright_lines = read_lines('copyrights/hardcoded')

    print(''.join(suround_with_stars(copyright_lines)))
    print()

    print(''.join(suround_with_number_symbols(copyright_lines)))
    print()

    print(''.join(comment_with_slash(copyright_lines)))
    print()

    print(''.join(comment_with_symbol_numbers(copyright_lines)))

if __name__ == '__main__':
    test_comments()