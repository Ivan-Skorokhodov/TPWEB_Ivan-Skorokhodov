from django.db import models
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.contrib.postgres.search import SearchVectorField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector

# Create your models here.


class QuestionManager(models.Manager):
    def get_new_questions(self):
        questions = self.all().annotate(likes=models.Count(
            'questionlike')).order_by("-created_at")[:30]
        tags = []
        for question in questions:
            tags.append(question.tags.values_list('title', flat=True))
        zipped = list(zip(questions, tags))
        return zipped

    def get_hot_questions(self):
        questions = self.all().annotate(likes=models.Count(
            'questionlike')).order_by("-likes")[:30]
        tags = []
        for question in questions:
            tags.append(question.tags.values_list('title', flat=True))
        zipped = list(zip(questions, tags))
        return zipped

    def get_question_by_question_id(self, question_id):
        return Question.objects.annotate(
            likes=models.Count('questionlike')).get(pk=question_id)

    def get_questions_by_tag(self, tag):
        questions = tag.question_set.all().annotate(likes=models.Count('questionlike'))
        tags = []
        for question in questions:
            tags.append(question.tags.values_list('title', flat=True))
        zipped = list(zip(questions, tags))
        return zipped


class AnswerManager(models.Manager):
    def get_answers_by_question(self, question):
        return Answer.objects.filter(question=question).annotate(
            is_correct=Exists(
                CorrectAnswer.objects.filter(answer=OuterRef('pk')))).annotate(
            likes=models.Count('answerlike')).order_by("-likes")

    def get_answer_by_answer_id(self, answer_id):
        return Answer.objects.annotate(
            likes=models.Count('answerlike')).get(pk=answer_id)


class TagManager(models.Manager):
    def get_tags_by_question(self, question):
        return question.tags.values_list('title', flat=True)

    def get_tag_by_title(self, tag_title):
        return Tag.objects.get(title=tag_title)


class Tag(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to='images')

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Question)
def update_search_vector(sender, instance, **kwargs):
    instance.search_vector = SearchVector('title', 'text')


class Answer(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=None)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return self.title


class CorrectAnswer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["profile", "answer"]


class AnswerLike(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["profile", "answer"]


class QuestionLike(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["profile", "question"]
