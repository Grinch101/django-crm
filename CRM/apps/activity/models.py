from django.db import models
import uuid

# Create your models here.
class Activities(models.Model):
    action = models.TextField('action')
    description = models.TextField('description')
    date = models.DateField('date')
    time = models.TimeField('time')
    contact_id = models.ForeignKey("contacts.Contacts", on_delete=models.CASCADE)
    user_id =models.ForeignKey("user.Users", on_delete=models.CASCADE)

    class Meta:
        db_table = 'activities'