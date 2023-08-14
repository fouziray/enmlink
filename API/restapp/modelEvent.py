# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from .models import Convo, DtSession
#class EventsManager(models.Manager):
   # def get_queryset(self):
       # return super().get_queryset().distinct('type_name')

class Events(models.Model):
    sender_id = models.CharField(max_length=255)
    #dtsession_id=models.ForeignKey(DtSession,on_delete=models.DO_NOTHING)
    #convo_id=models.ForeignKey(Convo, on_delete=models.CASCADE, related_name='messages')
    type_name = models.CharField(max_length=255)
    timestamp = models.FloatField(blank=True, null=True)
    intent_name = models.CharField(max_length=255, blank=True, null=True)
    action_name = models.CharField(max_length=255, blank=True, null=True)
    #data = models.TextField(blank=True, null=True)
    data = models.JSONField('data')  
    #objects = EventsManager()

    class Meta:
        managed = False
        db_table = 'events'
