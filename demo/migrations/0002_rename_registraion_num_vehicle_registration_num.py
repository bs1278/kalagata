# Generated by Django 3.2.14 on 2023-07-21 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='registraion_num',
            new_name='registration_num',
        ),
    ]