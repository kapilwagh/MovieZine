from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django import forms
from django.core.checks import messages
from django.conf import settings
# from django.db.models.signals import post_save

class Contact(models.Model):
    full_name=models.CharField(max_length=50, blank=True)
    email_id=models.EmailField(max_length=50, blank=True)
    message=models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.full_name



