from django.contrib.auth.models import User
from django.db import models


VISIBILITY_PUBLIC = 'PUB'
VISIBILITY_PRIVATE = 'PRI'

VISIBILITY = (
        (VISIBILITY_PUBLIC, 'Pública'),
        (VISIBILITY_PRIVATE, 'Privada')
    )


class Post(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    content = models.TextField(null=True, blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=3, choices=VISIBILITY, default=VISIBILITY_PUBLIC)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
