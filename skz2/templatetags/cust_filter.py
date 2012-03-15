#-*- coding: utf-8 -*-
#from django.template.defaultfilters import stringfilter
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import re
register = template.Library()

@register.filter
def user_mention(value, autoescape=None):
    user = re.match(r'@([\w]+)', value)
    if user is None:
        pass
    else:
        value= re.sub(r'@[\w]+', '<a href=https://twitter.com/#!/' + user.group(1) +'>@'+ user.group(1)+'</a>', value)
    return mark_safe(value)
user_mention.needs_autoescape = True

@register.filter
def hashtag(value, autoescape=None):
    hashtag = re.match(r'#([\w一-龠ぁ-んァ-ヴー]+)', value)
    if hashtag is None:
        pass
    else:
        value= re.sub(r'#[\w一-龠ぁ-んァ-ヴー]+', '<a href=https://twitter.com/#!/search/%23' + hashtag.group(1) +'>#'+ hashtag.group(1)+'</a>', value)
    return mark_safe(value)
hashtag.needs_autoescape = True
