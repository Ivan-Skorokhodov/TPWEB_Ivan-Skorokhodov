from django.core.management.base import BaseCommand
from app import models
from random import randint
from django.db import IntegrityError


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"]

        list_users = [
            models.User(
                username=f"User{i}", email=f"user{i}@example.com", password="password")
            for i in range(1, ratio + 1)
        ]
        models.User.objects.bulk_create(list_users)
        users = models.User.objects.all()

        self.stdout.write(f"Fill database with {ratio} users")

        list_profiles = [models.Profile(user=user) for user in users]
        models.Profile.objects.bulk_create(list_profiles)
        profiles = models.Profile.objects.all()

        self.stdout.write(f"Fill database with {ratio} profiles")

        list_tags = [models.Tag(title=f"Title{i}")
                     for i in range(1, ratio + 1)]
        models.Tag.objects.bulk_create(list_tags)

        self.stdout.write(f"Fill database with {ratio} tags")

        list_questions = [
            models.Question(
                title=f"Title{i}",
                content=f"Question content with id {i}",
                profile=profiles[i % len(profiles)]
            ) for i in range(1, ratio * 10 + 1)
        ]
        models.Question.objects.bulk_create(list_questions)

        tags = models.Tag.objects.all()
        start_pos_tag = 1
        for question in models.Question.objects.all():
            question_tags = [tags[i % len(tags)] for i in range(
                start_pos_tag, start_pos_tag + 5)]
            start_pos_tag += 5

            question.tags.add(*question_tags)

        self.stdout.write(f"Fill database with {ratio*10} questions")
        questions = models.Question.objects.all()
        list_answers = [
            models.Answer(
                title=f"Title{i}",
                content=f"Answer content with id {i}",
                profile=profiles[i % len(profiles)],
                question=questions[i % len(questions)],
            ) for i in range(1, ratio * 100 + 1)
        ]
        models.Answer.objects.bulk_create(list_answers)

        self.stdout.write(f"Fill database with {ratio*100} answers")

        answers = models.Answer.objects.all()

        # Добавление AnswerLike
        list_answerLikes = []
        set_answerLikes = set()

        for i in range(ratio * 100):
            new_profile = profiles[randint(0, len(profiles) - 1)]
            new_answer = answers[randint(0, len(answers) - 1)]

            # Проверка на уникальность, чтобы не было дубликатов
            while (new_profile, new_answer) in set_answerLikes:
                new_profile = profiles[randint(0, len(profiles) - 1)]
                new_answer = answers[randint(0, len(answers) - 1)]

            # Добавление пары профиля и ответа в список
            list_answerLikes.append(models.AnswerLike(
                profile=new_profile, answer=new_answer))
            if i % 1000 == 0:
                self.stdout.write(f"Fill database with {i} answerLikes")
            set_answerLikes.add((new_profile, new_answer))

        models.AnswerLike.objects.bulk_create(list_answerLikes)

        # Аналогично добавьте QuestionLike
        list_questionLikes = []
        set_questionLikes = set()

        for i in range(ratio * 100):
            new_profile = profiles[randint(0, len(profiles) - 1)]
            new_question = questions[randint(0, len(questions) - 1)]

            # Проверка на уникальность
            while (new_profile, new_question) in set_questionLikes:
                new_profile = profiles[randint(0, len(profiles) - 1)]
                new_question = questions[randint(0, len(questions) - 1)]

            list_questionLikes.append(models.QuestionLike(
                profile=new_profile, question=new_question))
            if i % 1000 == 0:
                self.stdout.write(f"Fill database with {i} questionLikes")
            set_questionLikes.add((new_profile, new_question))

        models.QuestionLike.objects.bulk_create(list_questionLikes)

        self.stdout.write(f"Fill database with {ratio} coefficient")
