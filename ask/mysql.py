#coding=utf8

from django.http import HttpResponse
from ask.models import Question, Answer
from django.contrib.auth.models import User
from django.utils import timezone
import random

def fill(request):
  contents = ""

  #create_users()
  #contents += "create_users<br>"
  
  users = User.objects.all()
  #create_questions(users)
  #contents += "create_questions<br>"
  
  questions = Question.objects.all()
  #create_answers(users, questions)
  #contents += "create_answers<br>"

  return HttpResponse("mysql filling script {<br>" + contents + "<br>};")

def create_users():
  for i in range(0, 10000):
    username = "dummy_user_" + str(i + 1);
    
    user = User(username=username, password="qwerty123", email="dummy@mail.ru")
    #user.set_password("qwerty123")
    user.save()

def create_questions(users):
  for i in range(0, 100000):
    uid = random.randint(0, len(users) - 1)
    
    question = Question(title="Doctor, where am i?", contents="With Black Jack and ladies of course", author=users[uid], date_created=timezone.now())
    question.save()

def create_answers(users, questions):
  for i in range(0, 1000000):
    uid = random.randint(0, len(users) - 1)
    qid = random.randint(0, len(questions) - 1)
    
    answer = Answer(contents="Просто ответ :|", question=questions[qid], author=users[uid], date_created=timezone.now())
    answer.save()
