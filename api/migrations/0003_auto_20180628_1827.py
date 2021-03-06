# Generated by Django 2.0.6 on 2018-06-28 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180628_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='db_adapter',
            field=models.CharField(default='postgres', max_length=256),
        ),
        migrations.AlterField(
            model_name='connection',
            name='host',
            field=models.CharField(default='localhost', max_length=64),
        ),
        migrations.AlterField(
            model_name='connection',
            name='port',
            field=models.IntegerField(default=5432),
        ),
    ]
