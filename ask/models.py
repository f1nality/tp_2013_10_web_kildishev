#coding=utf8

from django.db import models
from django.contrib.auth.models import User
from django import forms

class Question(models.Model):
    title = models.CharField(max_length=64)
    contents = models.TextField()
    author = models.ForeignKey(User)
    date_created = models.DateField()
    rating = models.IntegerField(db_index=True, default=0)

class Answer(models.Model):
    contents = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    date_created = models.DateField()
    is_right = models.BooleanField()
    rating = models.IntegerField()

class QuestionLike(models.Model):
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)
    is_up = models.BooleanField()

class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(User)
    is_up = models.BooleanField()

class AnswerForm(forms.Form):
    contents = forms.CharField(widget=forms.Textarea(attrs={"rows":4}))

class QuestionForm(forms.Form):
    title = forms.CharField(max_length=64)
    contents = forms.CharField(widget=forms.Textarea(attrs={"rows":4}))

class SignupForm(forms.Form):
    username = forms.CharField(max_length=64, label="логин")
    password = forms.CharField(label="пароль")
    password_confirmation = forms.CharField(label="подтверждение")
    email = forms.EmailField(label="e-почта")

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        email = cleaned_data.get("email")

        if User.objects.filter(username=username).count():
            self._errors["username"] = self.error_class(["Такой логин уже зарегистрирован"])

        if password != password_confirmation:
            self._errors["password"] = self.error_class(["Введенные пароли не совпадают"])

        if User.objects.filter(email=email).count():
            self._errors["email"] = self.error_class(["Такой email уже зарегистрирован"])

        return cleaned_data