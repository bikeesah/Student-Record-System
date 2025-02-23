# students/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    marks = models.FloatField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return self.name
