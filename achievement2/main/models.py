from django.db import models


# Create your models here.


class Number(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return self.number

    def update(self, new_number):
        self.number = new_number
