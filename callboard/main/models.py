from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_subscribed = models.BooleanField()


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class Advertisement(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    title = models.CharField(max_length=255)
    content = CKEditor5Field('Text', config_name='extends')
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True)
    response_text = models.TextField()
