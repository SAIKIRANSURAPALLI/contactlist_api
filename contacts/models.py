from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

class Contact(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    is_spam = models.BooleanField(default=False)
    spam_likelihood = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def mark_as_spam(self):
        self.is_spam = True
        self.save()
