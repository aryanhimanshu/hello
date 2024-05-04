from django.db import models

def URL_Model():
    long_url = models.CharField(max_length=1000, unique=True, primary_key=True)
    short_url = models.CharField(max_length=100, unique=True, db_index=True)
    visit_count = models.IntegerField(default=0)