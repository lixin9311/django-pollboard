import sys
from django import template

sys.path.append('../')

from polls.models import Choice, Vote

register = template.Library()

@register.filter
def getopt(choice, name):
    try:
        vote = choice.vote_set.get(name=name)
    except (KeyError, Vote.DoesNotExist):
        return 'X'
    else:
        return 'O'