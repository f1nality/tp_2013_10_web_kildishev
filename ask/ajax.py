from django.http import HttpResponse
from ask.models import Question, QuestionForm, QuestionLike, User
from django.utils import timezone

def question_like(request, id, value):
    id = int(id or 0)
    value = int(value or 0)

    if request.user.is_authenticated():
        if QuestionLike.objects.filter(question=id, author=request.user.id).count():
            return HttpResponse('error')
    else:
        return HttpResponse('error')

    question = Question.objects.get(id=id)

    if value == 0:
        question.rating -= 1
    else:
        question.rating += 1

    question.save()

    question_like = QuestionLike(question=question, author=request.user, is_up=(value != 0))
    question_like.save()

    return HttpResponse('{"rating": ' + str(question.rating) + '}')

def question_ask(request):
    question_form = QuestionForm(request.POST)
    if question_form.is_valid():

        title = question_form.cleaned_data["title"]
        contents = question_form.cleaned_data["contents"]

        question = Question(title=title, contents=contents, author=request.user, date_created=timezone.now())
        question.save()

        return HttpResponse('{"question_id": ' + str(question.id) + '}')
    else:
        error = ""

        for field in question_form:
            if field.errors:
                error += field.label_tag + ": " + field.errors + "<br>"

        return HttpResponse('{"error": "' + error + '"}')