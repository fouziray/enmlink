from django.contrib.auth.models import User
from ..models import Message, Convo, Connexion, HelpProvider
from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = ('id', 'username', 'first_name', 'last_name', 'email','password')

class HelpProviderSerialize(serializers.ModelSerializer):
     class Meta(UserSerializer.Meta):      
            model= HelpProvider
            fields= UserSerializer.Meta.fields+('fonction',)

class MessageSerializer(serializers.ModelSerializer):
     class Meta:
         model= Message
         fields=('user_id','convo_id','created','text','source_is_user')

class ConvoSerializer(serializers.ModelSerializer):
    class Meta:
         model= Convo
         fields=('user_id',)

class ConnexionSerializer(serializers.ModelSerializer):
    class Meta:
         model= Connexion
         fields=('help_provider','created','convo_id')

