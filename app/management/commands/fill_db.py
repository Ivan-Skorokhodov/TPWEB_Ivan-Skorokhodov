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

        list_answerLikes = [models.AnswerLike() for i in range(ratio * 100)]
        models.AnswerLike.objects.bulk_create(list_answerLikes)
        set_answerLikes = set()
        count = 0

        for answerLike in models.AnswerLike.objects.all():
            new_profile = profiles[randint(0, len(profiles) - 1)]
            new_answer = answers[randint(0, len(answers) - 1)]

            while (new_profile, new_answer) in set_answerLikes:
                new_profile = profiles[randint(0, len(profiles) - 1)]
                new_answer = answers[randint(0, len(answers) - 1)]

            answerLike.profile.add(new_profile)
            answerLike.answer.add(new_answer)
            set_answerLikes.add((new_profile, new_answer))

            count += 1
            self.stdout.write(
                f"Fill database with {count} answerLikes")

        list_questionLikes = [models.QuestionLike()
                              for i in range(ratio * 100)]
        models.QuestionLike.objects.bulk_create(list_questionLikes)
        set_questionLikes = set()
        count = 0

        for questionLike in models.QuestionLike.objects.all():
            new_profile = profiles[randint(0, len(profiles) - 1)]
            new_question = questions[randint(0, len(questions) - 1)]

            while (new_profile, new_question) in set_questionLikes:
                new_profile = profiles[randint(0, len(profiles) - 1)]
                new_question = questions[randint(0, len(questions) - 1)]

            questionLike.profile.add(new_profile)
            questionLike.question.add(new_question)
            set_questionLikes.add((new_profile, new_question))

            count += 1
            self.stdout.write(
                f"Fill database with {count} questionLikes")

        self.stdout.write(f"Fill database with {ratio} coefficient")
