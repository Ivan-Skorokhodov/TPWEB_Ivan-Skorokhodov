from django.shortcuts import render
from django.core.paginator import Paginator


QUESTIONS = []

for i in range(30):
    QUESTIONS.append({
        'title': f'Title {i}',
        'id': i,
        'content': f'Some very interesting text with id {i}'
    })

ANSWERS = []
for i in range(10):
    ANSWERS.append({
        'title': f'Title {i}',
        'id': i,
        'content': f'Some very interesting text with id {i}'
    })


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page', 1)
    page = paginator.page(page_num)

    return page


def index(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'index.html', {'questions': page.object_list, 'page_obj': page})


def hot(request):
    page = paginate(QUESTIONS, request)
    return render(request, 'hot.html', {'questions': page.object_list, 'page_obj': page})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')


def question(request, question_id):
    item = QUESTIONS[question_id]
    page = paginate(ANSWERS, request, 5)
    return render(request, 'question.html', {'question': item, 'answers': page.object_list, 'page_obj': page})
