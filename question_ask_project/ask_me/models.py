# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import AbstractUser
#
# from ask_me.managers import *
#
#
#
#
# class User(AbstractUser):
#     pass
#
#
#
#
# class Tag(models.Model):
#     name = models.CharField(max_length=20, default="404", verbose_name="Question's tag")
#
#     objects = TagManager()
#
#     def __str__(self):
#         return self.title
#
#
#
# class Question(models.Model):
#     author = models.ForeignKey(User, verbose_name="Question's owner")
#     title = models.CharField(max_length=50, verbose_name="Question's Header")
#     text = models.TextField(verbose_name="Question's Content")
#     date = models.DateTimeField(default=timezone.now(), verbose_name="Question's Date")
#     tags = models.ManyToManyField(Tag, related_name="question", blank=True, verbose_name="Question's Tags") #blank=True means Field can be empty (defalt value is False)
#     rating = models.IntegerField(default=0, null=False, verbose_name="Question's Rating")
#     is_active = models.BooleanField(default=True, verbose_name="Question's Availability")
#
#     objects = QuestionManager()
#
#     def __str__(self):
#         return self.title
#
#
#
# class Answer(models.Model):
#         author = models.ForeignKey(User, verbose_name="Answer's Owner")
#         date = models.DateTimeField(default=timezone.now(), verbose_name="Answer's Date")
#
#         question = models.ForeignKey(Question, verbose_name="Answer's Question")
#         text = models.TextField(verbose_name="Answer's Content")
#
#
#
#
#
#
#
#
#
#
#
# class Like():
#     pass