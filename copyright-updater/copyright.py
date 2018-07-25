from simple__repr__ import simple__repr__

class Copyright(object):

    def __init__(self, lines, comment_parameters):
        self.lines = lines
        self.comment_parameters = comment_parameters

    def __repr__(self):
        return simple__repr__(self)