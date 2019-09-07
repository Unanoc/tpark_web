from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ExifTags

from ask_me.managers import UserManager, TagManager, QuestionManager, AnswerManager, LikeDislikeManager


# AUTH_USER_MODEL set in settings
class User(AbstractUser):
    upload = models.ImageField(default="default/default_avatar.png", upload_to="uploads/%Y/%m/%d/", verbose_name="User's Avatar")
    registration_date = models.DateTimeField(default=timezone.now, verbose_name="User's Registration Date")
    rating = models.IntegerField(default=0, verbose_name="User's Rating")

    objects = UserManager()

    def __str__(self):
        return self.username

# functions for correct uploading avatar
def rotate_image(filepath):
    try:
        image = Image.open(filepath)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(filepath)
        image.close()
    except (AttributeError, KeyError, IndexError):
        pass

@receiver(post_save, sender=User, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
    if instance.upload:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fullpath = BASE_DIR + instance.upload.url
        rotate_image(fullpath)



class Tag(models.Model):
    name = models.CharField(max_length=20, default="404", verbose_name="Question's Tag")

    objects = TagManager()

    def __str__(self):
        return self.name


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name=("Vote"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=("User"))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

    def __str__(self):
        return self.user.username + " liked"


class Question(models.Model):
    author = models.ForeignKey(User, verbose_name="Question's Owner")
    title = models.CharField(max_length=50, verbose_name="Question's Header")
    text = models.TextField(verbose_name="Question's Content")
    date = models.DateTimeField(default=timezone.now, verbose_name="Question's Date")
    rating = models.IntegerField(default=0, null=False, verbose_name="Question's Rating")
    is_active = models.BooleanField(default=True, verbose_name="Question's Availability")
    tags = models.ManyToManyField(Tag, default=True, related_name='questions', verbose_name="Question's Tags")
    votes = GenericRelation(LikeDislike, related_query_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return self.text


class Answer(models.Model):
    author = models.ForeignKey(User, verbose_name="Answer's Owner")
    date = models.DateTimeField(default=timezone.now, verbose_name="Answer's Date")
    question = models.ForeignKey(Question, related_name='answers', verbose_name="Answer's Question")
    text = models.TextField(verbose_name="Answer's Content")
    rating = models.IntegerField(default=0, null=False, verbose_name="Answer's Rating")
    votes = GenericRelation(LikeDislike, related_query_name='answers')

    objects = AnswerManager()

    def __str__(self):
        return self.text