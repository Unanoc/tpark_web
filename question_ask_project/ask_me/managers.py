from django.db import models
from django.contrib.auth.models import UserManager


class User(UserManager):
    def by_username(self, username):
        return self.all().filter(username=username).first()


class QuestionManager(models.Model):

    def get_hot(self):
        return self.all().order_by('rating').reverse()

    def get_new(self):
        return self.all().order_by('date').reverse()

    def get_by_id(self, question_id):
        return self.all().filter(id=question_id)


class AnswerManager(models.Model):

    def get_answers(self):
        return self.all().order_by('date').reverse()


class TagManager(models.Model):
    def get_by_tag(self, tag_name):
        return self.filter(title=tag_name).first().questions.all().order_by('date').reverse()