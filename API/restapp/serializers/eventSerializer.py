from restapp.modelEvent import Events
from rest_framework import serializers

class EventSerialize(serializers.ModelSerializer):
     class Meta:
         model = Events
         fields = ('id', 'sender_id', 'type_name', 'timestamp', 'intent_name','action_name','data')

