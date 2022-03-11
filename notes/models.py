from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tags')

class Note(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    creation_date = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='notes')
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')

class TodoList(models.Model):
    title = models.CharField(max_length=64)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='todolists')


class Task(models.Model):
    text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE, null=True, related_name='tasks')