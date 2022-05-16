from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice


# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}

    return render(request, 'polls/index.html', context=context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }

    return render(request, 'polls/results.html', context=context)


def vote(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=question_id)

        try:
            voted = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            context = {
                'question': question,
                'error_message': "You didn't select a choice.",
            }
            return render(request, 'polls/detail.html', context=context)

        else:
            voted.up_votes()
            return HttpResponseRedirect(reverse('results', args=(question.id,)))


def add_poll(request):
    if request.method == "GET":
        return render(request, 'polls/new_poll.html')

    elif request.method == "POST":
        # new_question = Question(question_text=request.POST['title'][0]).save()
        # print(list(request.POST['choice[]']))
        body_dict = request.POST.getlist('choice[]')
        print(body_dict)
        # print(body_dict['choice[]'])
        # for i in body_dict['choice[]']:
        #     print(i)
            # Choice(question=new_question, choice_text=i).save()

        return HttpResponseRedirect(reverse('index'))
