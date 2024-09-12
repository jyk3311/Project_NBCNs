from django.db import models
from django.conf import settings

class Article(models.Model):

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_articles'
    )

    bookmarking = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='bookmarked'
    )

# Create your models here.
