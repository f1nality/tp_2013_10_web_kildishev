#coding=utf8

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from ask.models import Question, Answer, QuestionLike, AnswerLike, QuestionForm, AnswerForm, SignupForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import authenticate, login, logout

def index(request, tab, page):
    if tab != "popular":
        tab = "index"

    page = int(page or 0)

    if request.method == "POST" and request.user.is_authenticated():
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            title = question_form.cleaned_data["title"]
            contents = question_form.cleaned_data["contents"]

            question = Question(title=title, contents=contents, author=User.objects.get(id=request.user.id), date_created=timezone.now())
            question.save()

            return HttpResponseRedirect("/question/" + str(question.id))
    else:
        question_form = QuestionForm()

    if tab == "popular":
        questions = Question.objects.all().order_by("rating").reverse()
    else:
        questions = Question.objects.all().order_by("id").reverse()

    paginator = Paginator(questions, 20)

    try:
        questions = paginator.page(page)
    except EmptyPage:
        questions = paginator.page(1)

    for question in questions:
        question.answers_num = Answer.objects.filter(question=question.id).count()

        if request.user.is_authenticated():
            question.liked = QuestionLike.objects.filter(question=question.id, author=request.user.id).count()

    return render(request, "index.html", {"question_form": question_form, "tab": tab, "questions": questions, "page": page})

def process_login(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/index')
        else:
            return HttpResponse('disabled account')
    else:
        return HttpResponse('invalid login')

def process_logout(request):
    logout(request)

    return HttpResponseRedirect('/index')

def question(request, id):
    id = int(id or 0)

    if request.method == "POST" and request.user.is_authenticated():
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            title = question_form.cleaned_data["title"]
            contents = question_form.cleaned_data["contents"]

            question = Question(title=title, contents=contents, author=User.objects.get(id=request.user.id), date_created=timezone.now())
            question.save()

            return HttpResponseRedirect("/question/" + str(question.id))
    else:
        question_form = QuestionForm()

    question = Question.objects.get(id=id)
    answers = Answer.objects.filter(question=question.id)

    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            contents = answer_form.cleaned_data["contents"]

            answer = Answer(contents=contents, question=question, author=User.objects.get(id=1), date_created=timezone.now())
            answer.save()

            return HttpResponseRedirect("/question/" + id)
    else:
        answer_form = AnswerForm()

    return render(request, "question.html", {"question_form": question_form, "question": question, "answers": answers, "answer_form": answer_form})

def user(request, id):
    id = int(id or 0)

    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            title = question_form.cleaned_data["title"]
            contents = question_form.cleaned_data["contents"]

            question = Question(title=title, contents=contents, author=User.objects.get(id=1), date_created=timezone.now())
            question.save()

            return HttpResponseRedirect("/question/" + str(question.id))
    else:
        question_form = QuestionForm()

    profile = User.objects.get(id=id)
    questions = Question.objects.filter(author=id)[:20]
    answers = Answer.objects.filter(author=id)[:20]

    return render(request, "user.html", {"question_form": question_form, "profile": profile, "questions": questions, "answers": answers})

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index')

    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data["username"]
            password = signup_form.cleaned_data["password"]
            email = signup_form.cleaned_data["email"]

            user = User.objects.create_user(username, email, password)
            user.save()

            return HttpResponseRedirect("/user/" + str(user.id))
    else:
        signup_form = SignupForm()

    return render(request, "signup.html", {"signup_form": signup_form})
