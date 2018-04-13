from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from ask_me.managers import UserManager, TagManager, QuestionManager, AnswerManager, LikeManager


# AUTH_USER_MODEL set in settings
class User(AbstractUser):
    upload = models.ImageField(default="default/default_avatar.png", upload_to="uploads/%Y/%m/%d/", verbose_name="User's Avatar")
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="User's Registration Date")
    rating = models.IntegerField(default=0, verbose_name="User's Rating")

    objects = UserManager()

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=20, default="404", verbose_name="Question's Tag")

    objects = TagManager()

    def __str__(self):
        return self.name


# TODO with AJAX
class Like(models.Model):
    user = models.ForeignKey(User, null=False, db_column="author", verbose_name="Like's Author")
    is_liked = models.BooleanField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " liked"


class Question(models.Model):
    author = models.ForeignKey(User, verbose_name="Question's Owner")
    title = models.CharField(max_length=50, verbose_name="Question's Header")
    text = models.TextField(verbose_name="Question's Content")
    date = models.DateTimeField(default=timezone.now, verbose_name="Question's Date")
    rating = models.IntegerField(default=0, null=False, verbose_name="Question's Rating")
    is_active = models.BooleanField(default=True, verbose_name="Question's Availability")
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name="Question's Tags")

    objects = QuestionManager()

    def __str__(self):
        return self.text


class Answer(models.Model):
    author = models.ForeignKey(User, verbose_name="Answer's Owner")
    date = models.DateTimeField(default=timezone.now, verbose_name="Answer's Date")
    question = models.ForeignKey(Question, related_name='answers', verbose_name="Answer's Question")
    text = models.TextField(verbose_name="Answer's Content")
    rating = models.IntegerField(default=0, null=False, verbose_name="Answer's Rating")

    objects = AnswerManager()

    def __str__(self):
        return self.text