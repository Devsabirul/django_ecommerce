from django.db import models
from django.contrib.auth.models import User


class VerificationCode(models.Model):
    code = models.CharField(max_length=4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
