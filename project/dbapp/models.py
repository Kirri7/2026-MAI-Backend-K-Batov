from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='authored_courses'
    )
    students = models.ManyToManyField( # обещают UNIQUE (user_id, course_id)
        User, 
        related_name='enrolled_courses'
    )

class Admin(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30, unique=True)
