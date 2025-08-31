from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    time_commitment = models.IntegerField(help_text="Hours per week")
    free_time_start = models.TimeField()
    free_time_end = models.TimeField()

    def __str__(self):
        return f"{self.user.username}'s Profile"