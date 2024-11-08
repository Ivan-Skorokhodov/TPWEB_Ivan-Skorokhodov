from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponseBadRequest
from app import models


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page', 1)

    try:
        page_num = int(page_num)
    except ValueError:
        return HttpResponseBadRequest("Invalid page number")

    try:
        page = paginator.page(page_num)
    except InvalidPage:
        return HttpResponseBadRequest("Page does not exist")

    return page


def index(request):
    zipped_questions_tags = models.Question.objects.get_new_questions()
    page = paginate(zipped_questions_tags, request)
    if isinstance(page, HttpResponseBadRequest):
        return page
    return render(request, 'index.html', {'zipped': page.object_list, 'page_obj': page})


def hot(request):
    zipped_questions_tags = models.Question.objects.get_hot_questions()
    page = paginate(zipped_questions_tags, request)
    if isinstance(page, HttpResponseBadRequest):
        return page
    return render(request, 'hot.html', {'zipped': page.object_list, 'page_obj': page})


def tag(request, tag_title):
    tag = models.Tag.objects.get_tag_by_title(tag_title)
    zipped_questions_tags = models.Question.objects.get_questions_by_tag(tag)
    page = paginate(zipped_questions_tags, request)
    if isinstance(page, HttpResponseBadRequest):
        return page
    return render(request, 'tag.html', {'zipped': page.object_list, 'tag': tag, 'page_obj': page})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def question(request, question_id):
    question = models.Question.objects.get_question_by_question_id(question_id)
    tags = models.Tag.objects.get_tags_by_question(question)
    answers = models.Answer.objects.get_answers_by_question(question)
    page = paginate(answers, request, 5)
    if isinstance(page, HttpResponseBadRequest):
        return page
    return render(request, 'question.html', {'question': question, 'answers': page.object_list, 'tags': tags, 'page_obj': page})
