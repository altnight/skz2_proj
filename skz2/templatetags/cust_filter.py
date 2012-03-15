#-*- encofing:utf-8 -*-
#from django.template.defaultfilters import stringfilter
from django import template

import re
register = template.Library()

@register.filter
#@stringfilter
def user_mention(value):
    user = re.match(r'(@[\w]+)', value)
    if user is None:
        pass
    else:
        value= re.sub(r'@[\w]+', '<a href="https://twitter.com/#!/">user.group(1)</a>', value)
    #if re.match(r'@[\w]+', value):
        #re.sub(, , value)
    return value
#user_mention.is_safe=False
#register.filter(user_mention)
