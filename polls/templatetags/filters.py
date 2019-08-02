import sys
from django import template

sys.path.append('../')

from polls.models import Choice, Vote

register = template.Library()

@register.filter
def getopt(choice, name):
    print('---------------------------------')
    print(choice)
    print(name)
    print('---------------------------------')
    try:
        vote = choice.vote_set.get(name=name)
        print(vote)
        print('---------------------------------')
    except (KeyError, Vote.DoesNotExist):
        return 'X'
    else:
        return 'O'