from django.utils.translation import ugettext as _


class MissingActionParam(Exception):
    def __init__(self, scope, param):
        Exception.__init__(self, _("'%s' param not provided for '%s'" % (
            param, scope
        )))
