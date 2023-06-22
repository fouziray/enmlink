from django.contrib.auth.models import User
from ..models import Convo, Connexion, HelpProvider #Message

from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = ('id', 'username', 'first_name', 'last_name', 'email','password')
     
     def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class HelpProviderSerialize(serializers.ModelSerializer):
     class Meta(UserSerializer.Meta):      
            model= HelpProvider
            fields= UserSerializer.Meta.fields+('fonction',)

"""class MessageSerializer(serializers.ModelSerializer):
     class Meta:
         model= Message
         fields=('user_id','convo_id','created','text','source_is_user')
"""
class ConvoSerializer(serializers.ModelSerializer):
    class Meta:
         model= Convo
         fields=('user_id',)

class ConnexionSerializer(serializers.ModelSerializer):
    class Meta:
         model= Connexion
         fields=('help_provider','created','convo_id')

