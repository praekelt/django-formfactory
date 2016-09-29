from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from formfactory import validators


@validators.register
def dummy_validator(value):
    if value % 2:
        raise ValidationError(
            _("%(value) is not divible by 2"), params={"value": value}
        )
    return True
