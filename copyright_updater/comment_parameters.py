from .simple__repr__ import simple__repr__

class CommentParameters(object):

    def __init__(self, comment_type, symbol, additional_spaces_before_begin_symbol=1, additional_spaces_after_begin_symbol=1,
        additional_spaces_before_end_symbol=2):
        
        self.comment_type = comment_type
        self.symbol = symbol
        self.additional_spaces_before_begin_symbol = additional_spaces_before_begin_symbol
        self.additional_spaces_after_begin_symbol = additional_spaces_after_begin_symbol
        self.additional_spaces_before_end_symbol = additional_spaces_before_end_symbol

    def __repr__(self):
        return simple__repr__(self)