from django.db import models
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
