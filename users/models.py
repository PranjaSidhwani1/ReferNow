from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('referrer', 'Referrer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.role}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
    
class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('employed', 'Employed'),
        ('self_employed', 'Self Employed'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=15, blank=True)
    current_location = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)

    company = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    def __str__(self):
        return self.user.username