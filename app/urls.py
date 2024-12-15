from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/<str:tag_title>', views.tag, name='tag'),
    path('like/<int:question_id>',
         views.like_question_async, name='question_like'),
    path('answerLike/<int:answer_id>',
         views.like_answer_async, name='aswer_like'),
    path('correct/<int:answer_id>',
         views.correct_answer_async, name='aswer_correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
