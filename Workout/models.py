from django.contrib.auth.models import User
from django.db import models

class Exercise(models.Model):
    # Name of the exercise ("bench press")
    name = models.CharField(max_length=100)

    # Illustration of the exercise (optional)
    illustration = models.ImageField(upload_to='images/', null=True, blank=True)

    # Link Exercise to User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Performance(models.Model):
    # Exercise related
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    # Date of the exercise
    date = models.DateField(auto_now_add=True)

    # Repetitions related
    repetitions = models.JSONField()

    # Weights related
    weight = models.JSONField()

    def __str__(self):
        return f'{self.exercise.name} - {self.date}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # To determine age
    birth_date = models.DateField(null=True, blank=True)

    # Weight
    weight = models.FloatField(null=True, blank=True)

    # Activity level (description of activity, e.g., sedentary, active)
    activity = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
