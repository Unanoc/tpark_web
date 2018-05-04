from django.db import models
from django.contrib.auth.models import UserManager
from django.db.models import Sum


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

    def get_hot_for_answer(self, question_id):
        return self.all().filter(question_id=question_id).order_by('rating').reverse()

    def get_all_hot(self):
        return self.all().order_by('rating').reverse()


class TagManager(models.Manager):

    def get_by_tag(self, tag_name):
        return self.filter(name=tag_name).first().questions.all().order_by('date').reverse()


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def questions(self):
        return self.get_queryset().filter(content_type__model='question').order_by('-question__pub_date')

    def answers(self):
        return self.get_queryset().filter(content_type__model='answer').order_by('-answer__pub_date')