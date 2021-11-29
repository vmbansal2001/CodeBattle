from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

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

class Player(models.Model):
    prev = models.ForeignKey('BattleZone.Player', related_name='prev1', on_delete=models.SET_NULL, null=True)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    next = models.ForeignKey('BattleZone.Player', related_name='next1', on_delete=models.SET_NULL, null=True)
    in_room = models.ForeignKey('BattleZone.Room',on_delete=models.CASCADE,null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return "Player - " + self.player.first_name + " (" + self.player.username + ")"

class Room(models.Model):
    room_code = models.IntegerField(primary_key=True)
    room_admin = models.CharField(max_length=100)
    no_of_questions = models.IntegerField(default=3)
    date = models.DateField()
    currentPlayersCount = models.IntegerField(default=0)

    head = models.ForeignKey('BattleZone.Player', related_name='head', on_delete=models.CASCADE, null=True)
    tail = models.ForeignKey('BattleZone.Player', related_name='tail', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.room_code)
