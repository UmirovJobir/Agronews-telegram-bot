from distutils.text_file import TextFile
from statistics import mode
from django.db import models

class User(models.Model):
    chat_id = models.IntegerField()
    name = models.CharField(max_length=30)
    phone = models.IntegerField()
    link = models.URLField(blank=True, null=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text