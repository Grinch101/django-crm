from django.db import models


# Create your models here.
class Users(models.Model):
    client_name = models.TextField('client_name')
    email = models.TextField('email', unique=True)
    passkey = models.TextField('passkey')
    
    class Meta:
        db_table = 'users'