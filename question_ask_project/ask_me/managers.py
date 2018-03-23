from django.db import models
from django.contrib.auth.models import UserManager


class UserManager(UserManager):

    def by_username(self, username):
        return self.all().filter(username=username).first()


class QuestionManager(models.Manager):

    def get_hot(self):
        return self.all().order_by('rating').reverse()

    def get_new(self):
        return self.all().order_by('date').reverse()

    def get_by_id(self, question_id):
        return self.all().filter(id=question_id)


class AnswerManager(models.Manager):

    def get_answers_hot(self):
        return self.all().order_by('rating').reverse()


class TagManager(models.Manager):

    def get_by_tag(self, tag_name):
        return self.filter(name=tag_name).first().questions.all().order_by('date').reverse()


class LikeManager(models.Manager):
    #TODO
    pass