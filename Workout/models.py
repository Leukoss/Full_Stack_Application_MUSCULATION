from django.contrib.auth.models import User
from django.db import models
import uuid
from django.core.exceptions import ValidationError

class Exercise(models.Model):

    # id of execrise that could identify an exercise - string
    exercise_id = models.CharField(max_length=30,unique=True,null=True)
    
    # Name of the exercise ("bench press")
    name = models.CharField(max_length=100)

    # Illustration of the exercise (optional)
    illustration = models.ImageField(upload_to='images/', null=True, blank=True)

    # Link Exercise to User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # to generate a unique id for each exercise if is not specifier
    def save(self, *args, **kwargs):
        if not self.exercise_id:
            self.exercise_id = str(uuid.uuid4())[:8]
        super().save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.name} - {self.user}'

class Performance(models.Model):
    # Exercise related
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    # Date of the exercise
    date = models.DateField(auto_now_add=True)

    # Repetitions related
    repetitions = models.JSONField()

    # Weights related
    weights = models.JSONField()

    # to keep the same ammount of set of weights and repetitions
    def save(self, *args, **kwargs):
        if len(self.repetitions) != len(self.weights):
            raise ValueError("Les longueurs des répétitions et des poids doivent être identiques.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.exercise.name} - {self.date}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # gender of user - man / woman / other
    gender = models.CharField(max_length=100, default="A" )

    # To determine age
    age = models.IntegerField(null=True, blank=True)

    # Weight (kg)
    weight = models.FloatField(null=True, blank=True)

    # Height (cm)
    height = models.FloatField(null=True, blank=True)

    # Activity level (description of activity, e.g., sedentary, active)
    activity = models.CharField(max_length=100)

    # Country of residence
    country = models.CharField(max_length=100, default="France")

    # IMC
    bmi = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def calculate_bmi(self):
        if self.weight and self.height:
            return round(self.weight / ((self.height / 100) **2), 2)
        return None
    
    def clean(self):
        super().clean()
        if self.age < 0:
            raise ValidationError({'age': "L'âge ne peut pas être négatif."})
        
    def save(self, *args, **kwargs):
        self.bmi = self.calculate_bmi()
        super(UserProfile, self).save(*args, **kwargs)
