from django.db import models


class Exploit(models.Model):
    """
    The object Exploit which is uniquely identified with a numerical ID
    """
    id = models.IntegerField(primary_key=True)
    file = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.TextField()
    type = models.TextField()
    platform = models.TextField()
    port = models.TextField()


class Shellcode(models.Model):
    """
    The object Shellcode which is uniquely identified with a numerical ID
    """
    id = models.IntegerField(primary_key=True)
    file = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.TextField()
    type = models.TextField()
    platform = models.TextField()


class Suggestion(models.Model):
    """
    The object Suggestion is used to help the user to search for the most common results.
    """
    id = models.AutoField(primary_key=True)
    searched = models.TextField(null=False, blank=False, unique=True)
    suggestion = models.TextField(null=False, blank=False)
    autoreplacement = models.BooleanField(null=False)
