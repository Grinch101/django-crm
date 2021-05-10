from django.db import models


# Create your models here.
class Users(models.Model):
    client_name = models.TextField('client_name')
    email = models.TextField('email', unique=True)
    passkey = models.TextField('passkey')
    
    def __str__(self):
        return f'{self.id} , {client_name}, {email}, {passkey}'
    class Meta:
        db_table = 'users'
    
