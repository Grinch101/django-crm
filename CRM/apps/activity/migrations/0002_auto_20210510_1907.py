# Generated by Django 3.2.2 on 2021-05-10 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('contacts', '0002_alter_contacts_user_id'),
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='contact_id',
            field=models.ForeignKey(db_column='contact_id', on_delete=django.db.models.deletion.CASCADE, to='contacts.contacts'),
        ),
        migrations.AlterField(
            model_name='activities',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='user.users'),
        ),
    ]
