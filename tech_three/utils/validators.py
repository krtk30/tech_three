from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message=_("Phone number must be entered in the format: '+999999999'. "
                                       "Up to 15 digits allowed."))

NAME_REGEX = RegexValidator(regex=r'^([a-zA-Z0-9-.,&]+\s)*[a-zA-Z0-9-.,&]+$',
                            message=_('The following special characters are restricted: '
                                      '@, #, $, %, ?, (, ), *, !, ^, [, ], {, }, “, <, >, /, '))
