from django.db import models


class Exploit(models.Model):
    id = models.IntegerField(primary_key=True)
    file = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.TextField()
    vulnerability_type = models.TextField()
    platform = models.TextField()
    port = models.IntegerField(blank=True)


class Shellcode(models.Model):
    id = models.IntegerField(primary_key=True)
    file = models.TextField()
    description = models.TextField()
    date = models.DateField()
    author = models.TextField()
    vulnerability_type = models.TextField()
    platform = models.TextField()
