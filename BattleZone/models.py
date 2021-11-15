from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL

class PersonalInfo2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    City = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    OCCUPATION_CHOICES = [
        ('STU', 'Student'),
        ('PRO', 'Professional'),
        ('OTR', 'Other'),
    ]

    Occupation = models.CharField(max_length=3, choices=OCCUPATION_CHOICES)

    LANGUAGE_CHOICES = [
        ('CPP', 'C++'),
        ('JAVA', 'Java'),
        ('PYTHON', 'Python'),
    ]

    PreferredProgrammingLanguage = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

class Room(models.Model):
    room_code = models.IntegerField(primary_key=True)
    room_admin = models.CharField(max_length=100)
    no_of_questions = models.IntegerField(default=3)
    no_of_players = models.IntegerField(default=1)
    date = models.DateField()
    players = []
    for player in range(1):
        players.append(models.ForeignKey('User', on_delete=SET_NULL, null=True))

    def __str__(self):
        return str(self.room_code)
