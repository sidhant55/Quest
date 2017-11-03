from django.db import models

"""
user class is used to save user's credential 
parameter
    name  = storing the name of the user
    email = storint the email of the user
    key   = (not from management command) user provided key

"""

class user(models.Model):

    def __str__(self):
        return str(self.name)

    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100, null=True)
    key=models.CharField(max_length=100)
