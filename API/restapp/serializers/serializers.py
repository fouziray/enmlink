from django.contrib.auth.models import User
from ..models import Convo, Connexion, HelpProvider,ManagedObject, Profile, Technology #Message

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

class ManagedObjectStateSerializer(serializers.ModelSerializer):
    class Meta:
        model= ManagedObject
        fields=('state',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields=('avatar',)

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model= Technology
        fields=['auto_increment_id','type','state']

class SiteSerializer(serializers.ModelSerializer):
    #technologies= serializers.StringRelatedField(many=True)
    #tech = TechnologySerializer()
    managedObject=TechnologySerializer(many=True)
    
    class Meta:
        model= ManagedObject
        fields=['site_id','wilaya','UOP','managedObject']
    def create(self, validated_data):
        technologies_data = validated_data.pop("managedObject")
        mo = ManagedObject.objects.create(**validated_data)
        technology_serializer = self.fields['managedObject']
        for technology_data in technologies_data:
            technology_data['managedObject'] = mo
            Technology.objects.create(**technology_data)
        #techno= technology_serializer.create(technologies_data)
        return mo



