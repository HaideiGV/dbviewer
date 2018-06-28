from django.db import models
from api.constants import POSTGRES_ADAPTER


class Connection(models.Model):
    db_adapter = models.CharField(max_length=256, null=False, default=POSTGRES_ADAPTER)
    host = models.CharField(max_length=64, null=False, default='localhost')
    port = models.IntegerField(default=5432)
    username = models.CharField(max_length=256, null=False)
    password = models.CharField(max_length=256, null=False)
    db_name = models.CharField(max_length=256, null=False)
