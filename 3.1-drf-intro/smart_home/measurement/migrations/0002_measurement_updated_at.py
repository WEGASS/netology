# Generated by Django 4.1 on 2022-09-20 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
