
class MissingActionParam(Exception):
    def __init__(self, scope, param):
        Exception.__init__(self, "'%s' param not provided for '%s'" % (
            param, scope
        ))
