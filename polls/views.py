from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Vote

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    votes = question.vote_set.all()
    names = {}
    for voted in votes:
        names[voted.name] = 1
    names = list(names.keys())
    return render(request, 'results.html', {'question': question, 'names': names})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    selected_choices = []
    try:
        choices = request.POST.getlist('choice')
        for cid in choices:
            selected_choice = question.choice_set.get(pk=cid)
            selected_choices.append(selected_choice)
        voter_name = request.POST['name']
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a valid choice.",
        })
    else:
        votes = []
        for choice in selected_choices:
            choice.votes += 1
            choice.save()
            voted = Vote(name=voter_name, question=question,choice=choice)
            voted.save()
            votes.append(voted)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))