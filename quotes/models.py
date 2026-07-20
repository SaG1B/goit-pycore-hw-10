from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    fullname = models.CharField(max_length=150, unique=True)
    born_date = models.CharField(max_length=50, blank=True, null=True)
    born_location = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    tags = models.ManyToManyField(Tag, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.quote[:50]}..." by {self.author.fullname}'