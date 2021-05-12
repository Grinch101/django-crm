from django.db import models
import uuid
from django.contrib.postgres.fields import HStoreField


class Contacts(models.Model):
    FirstName = models.TextField('First Name')
    LastName = models.TextField('Last Name')
    Email = HStoreField('E-mail Addresses', null=True)
    PhoneNumber = HStoreField('Phone Number', null=True)
    user_id = models.ForeignKey("user.Users", on_delete=models.CASCADE, db_column='user_id')

    class Meta:
        db_table = 'contacts'