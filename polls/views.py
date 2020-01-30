from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question, Choice 
from django.utils import timezone
from django.contrib import messages

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def add(request):
    context = {}
    return render(request, 'polls/add.html', context)

def new(request):
    tmp = ""
    if request.method == 'POST':
        question = request.POST.get('question')
        choice1 = request.POST.get('choice1')
        choice2 = request.POST.get('choice2')
        choice3 = request.POST.get('choice3')
        choice4 = request.POST.get('choice4')
        question_object = Question.objects.create(question_text=question,pub_date=timezone.now())
        question_object.choice_set.create(choice_text=choice1,votes=0)
        question_object.choice_set.create(choice_text=choice2,votes=0)
        question_object.choice_set.create(choice_text=choice3,votes=0)
        question_object.choice_set.create(choice_text=choice4,votes=0)
        tmp = "Poll Created Successfully!!"
    else:
        tmp = "Some Error Occured!!"
    messages.add_message(request,messages.INFO,tmp)
    return HttpResponseRedirect(reverse('polls:add'))
        
