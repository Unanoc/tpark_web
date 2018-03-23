from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.utils import timezone
from ask_me.models import *

#To clean up Data base and generate fake data just write "python manage.py fake_generator

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = self.user_generate()
        tags = self.tag_generator()
        questions = self.question_generate(users=users, tags=tags)
        self.answer_generate(questions=questions, users=users)



    def user_generate(self):
        User.objects.all().delete()
        list_of_users = []

        faker = Faker()
        for i in range(1, 10):
            username = "User " + str(i)
            user = User.objects.create_user(username=username, password=username)

            first_name, last_name = faker.name().split(' ')
            user.first_name = first_name
            user.last_name = last_name
            user.rating = random.randint(1, 100)
            user.save()
            list_of_users.append(user)
        return list_of_users



    def tag_generator(self):
        Tag.objects.all().delete()
        list_of_tags = []

        faker = Faker()
        for i in range(1, 30):
            word = faker.sentence().split(' ')[1]
            tags = Tag.objects.create(name=word)
            tags.save()
            list_of_tags.append(tags)
        return list_of_tags



    def question_generate(self, users, tags):
        Question.objects.all().delete()
        list_of_questions = []

        faker = Faker()
        for i in range(1, 100):
            user = random.choice(users)
            question = Question.objects.create(author=user)

            for tag in range(3):
                tag = random.choice(tags)
                question.tags.add(tag)

            question.title = faker.sentence()[:random.randint(15,50)]
            question.text = faker.text()
            question.rating = random.randint(1, 100)
            question.save()
            list_of_questions.append(question)
        return list_of_questions



    def answer_generate(self, questions, users):
        Answer.objects.all().delete()

        faker = Faker()
        for i in range(1, 200):
            user = random.choice(users)
            question = random.choice(questions)
            answer = Answer.objects.create(author=user, question=question)

            answer.text = faker.text()
            answer.rating = random.randint(1, 100)
            answer.save()