from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms.formsets import formset_factory

from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm, BaseChoiceFormSet


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
        post = request.POST
        question_text = post.get('title')
        choices = post.getlist('choice_text')

        question_form = QuestionForm(post)

        ChoiceFormSet = formset_factory(ChoiceForm, formset=BaseChoiceFormSet, validate_min=2)
        data = {
            'form-TOTAL_FORMS': str(len(choices)),
            'form-INITIAL_FORMS': '0',
        }

        for i, c in enumerate(choices):
            data[f'form-{i}-choice_text'] = c

        choice_formset = ChoiceFormSet(data)

        print(question_form.is_valid(), choice_formset.is_valid())

        if question_form.is_valid() and choice_formset.is_valid():
            new_question = Question(question_text=question_text)
            new_question.save()

            for i in choices:
                Choice(question=new_question, choice_text=i).save()

            print("validation and save complete")

            return HttpResponseRedirect(reverse('index'))

        else:
            print(choice_formset.errors)
            return HttpResponse("question or choices are not valid.")
