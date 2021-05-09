from django.db import models
import uuid

# Create your models here.
class Contacts(models.Model):
    name = models.TextField('name')
    phone = models.TextField('phone')
    user_id = models.ForeignKey("user.Users", on_delete=models.CASCADE)

    class Meta:
        db_table = 'contacts'