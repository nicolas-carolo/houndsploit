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
    vulnerability_type = models.TextField()
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
    vulnerability_type = models.TextField()
    platform = models.TextField()
