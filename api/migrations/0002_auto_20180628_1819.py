# Generated by Django 2.0.6 on 2018-06-28 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='port',
            field=models.IntegerField(),
        ),
    ]
