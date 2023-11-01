from django.db import models
from django.conf import settings


class Stone(models.Model):
    Stone_ID = models.AutoField(primary_key=True, unique=True)
    Stone_Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Stone_Name


class Activation(models.Model):
    Activation_ID = models.AutoField(primary_key=True, unique=True)
    User_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Stone_ID = models.ForeignKey(Stone, on_delete=models.CASCADE)
    Start_Time = models.DateTimeField()
    End_Time = models.DateTimeField()

    def __str__(self):
        return f"Activation {self.Activation_ID} - {self.User_ID.username} - {self.Stone_ID.Stone_Name}"
