from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    remind_at = models.DateTimeField()

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.remind_at}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    time_commitment = models.IntegerField(help_text="Hours per week")
    free_time_start = models.TimeField()
    free_time_end = models.TimeField()

    def __str__(self):
        return f"{self.user.username}'s profile"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    time_commitment = models.IntegerField(help_text="Hours per week")
    free_time_start = models.TimeField()
    free_time_end = models.TimeField()

    def __str__(self):
        return f"{self.user.username}'s profile"

class MakeTimeItem(models.Model):
    CATEGORY_CHOICES = [
        ('hobby', 'Hobby'),
        ('person', 'Person'),
        ('work', 'Work'),
        ('self', 'Self'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    label = models.CharField(max_length=100)  # e.g. "Painting", "Mom", "Meditation"
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.label}"