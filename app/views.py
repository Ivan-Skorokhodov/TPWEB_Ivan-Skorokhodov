from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponseBadRequest
from app import models
from app import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from cent import Client, PublishRequest


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
    form = forms.LoginForm
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return render(request, 'settings.html', {'form': forms.SettingsForm()})
            form.add_error(None, 'Invalid username or password')

    return render(request, 'login.html', {'form': form})


def signup(request):
    form = forms.SignupForm
    if request.method == 'POST':
        form = forms.SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return render(request, 'settings.html', {'form': forms.SettingsForm()})

    return render(request, 'signup.html', {'form': form})


@login_required
def ask(request):
    form = forms.AskForm
    if request.method == 'POST':
        form = forms.AskForm(request.POST)
        if form.is_valid():
            answerForm = forms.AnswerForm
            question = form.save(request)
            tags = models.Tag.objects.get_tags_by_question(question)
            answers = models.Answer.objects.get_answers_by_question(question)
            page = paginate(answers, request, 5)
            if isinstance(page, HttpResponseBadRequest):
                return page
        return render(request, 'question.html', {'question': question, 'answers': page.object_list, 'tags': tags, 'page_obj': page, 'form': answerForm})

    return render(request, 'ask.html', {'form': form})


@login_required
def settings(request):
    form = forms.SettingsForm(instance=request.user)
    if request.method == 'POST':
        form = forms.SettingsForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'settings.html', {'form': form})
    return render(request, 'settings.html', {'form': form})


def logout(request):
    auth.logout(request)
    return render(request, 'login.html', {'form': forms.LoginForm()})


@login_required
def question(request, question_id):
    form = forms.AnswerForm
    question = models.Question.objects.get_question_by_question_id(question_id)
    tags = models.Tag.objects.get_tags_by_question(question)
    answers = models.Answer.objects.get_answers_by_question(question)
    page = paginate(answers, request, 5)
    if isinstance(page, HttpResponseBadRequest):
        return page

    if request.method == 'POST':
        form = forms.AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(request, question)

            profile = answer.profile
            if profile.avatar:
                avatar = profile.avatar.url
            else:
                avatar = "/uploads/images/default.jpg"

            api_url = "http://localhost:8010/api"
            api_key = "my_api_key"

            client = Client(api_url, api_key)
            centifugo_request = PublishRequest(channel=str(question_id), data={
                "avatar": avatar, "likes": 0, "answer_id": answer.id, "title": answer.title, "content": answer.content, "is_correct": False})
            client.publish(centifugo_request)

            return render(request, 'question.html', {'question': question, 'answers': page.object_list, 'tags': tags, 'page_obj': page, 'form': form})

    return render(request, 'question.html', {'question': question, 'answers': page.object_list, 'tags': tags, 'page_obj': page, 'form': form})


@require_http_methods(['POST'])
@login_required
def like_question_async(request, question_id):
    user = request.user
    question_like, created = models.QuestionLike.objects.get_or_create(
        profile=models.Profile.objects.get(user=user),
        question=models.Question.objects.get(pk=question_id)
    )
    if not created:
        question_like.delete()

    question = models.Question.objects.get_question_by_question_id(question_id)

    return JsonResponse({'likesCount': question.likes})


@require_http_methods(['POST'])
@login_required
def like_answer_async(request, answer_id):
    user = request.user
    answer_like, created = models.AnswerLike.objects.get_or_create(
        profile=models.Profile.objects.get(user=user),
        answer=models.Answer.objects.get(pk=answer_id)
    )
    if not created:
        answer_like.delete()

    answer = models.Answer.objects.get_answer_by_answer_id(answer_id)

    return JsonResponse({'likesCount': answer.likes})


@require_http_methods(['POST'])
@login_required
def correct_answer_async(request, answer_id):
    user = request.user
    answer = models.Answer.objects.get(pk=answer_id)

    if user == answer.profile.user:
        correct_answer, created = models.CorrectAnswer.objects.get_or_create(
            profile=models.Profile.objects.get(user=user),
            answer=answer
        )
        if not created:
            correct_answer.delete()
            return JsonResponse({'isCorrect': False})
        return JsonResponse({'isCorrect': True})

    return JsonResponse({'isCorrect': False})
