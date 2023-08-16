from django.contrib.auth.models import User
from ..models import Convo, Connexion, HelpProvider,ManagedObject, Profile, Technology, DtSession #Message

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
         model = User
         fields = ('id', 'username', 'first_name', 'last_name', 'email','password','last_login')
     
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

class DTserializercreation(serializers.ModelSerializer):
    title=serializers.CharField(source='site_id')
    startDate=serializers.DateTimeField(source='start_time')
    endDate=serializers.DateTimeField(source='end_Time')
    class Meta:
        model= DtSession
        fields = ['dtTeam_id' , 'technicien_id' , 'startDate' , 'endDate','id','title']
class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        depth = 1
        fields = '__all__'

class DTSerializer(serializers.ModelSerializer):
    #title=serializers.SerializerMethodField('get_alternate_name_code_site')
    #startDate= serializers.SerializerMethodField('get_alternate_name_start')
    #endDate= serializers.SerializerMethodField('get_alternate_name_end')
    title=serializers.CharField(source='site_id')
    startDate=serializers.DateTimeField(source='start_time')
    endDate=serializers.DateTimeField(source='end_Time')

    class Meta:
        model= DtSession
        depth = 1
        fields=['dtTeam' , 'technicien' , 'startDate' , 'endDate','id','title']
    def get_alternate_name_code_site(self,obj):
        return obj.site.site_id
    def get_alternate_name_start(self,obj):
        return obj.start_time
    def get_alternate_name_end(self,obj):
        return obj.end_Time

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
        mo, created = ManagedObject.objects.get_or_create(**validated_data)
        technology_serializer = self.fields['managedObject']

        if(created):
            for technology_data in technologies_data:
                technology_data['managedObject'] = mo
                Technology.objects.create(**technology_data)
            #techno= technology_serializer.create(technologies_data)
        
        return mo


class SiteSerializer2(serializers.ModelSerializer):
  
    session=DTSerializer(many=True)
    
    class Meta:
        model= ManagedObject
        fields=['site_id','wilaya','UOP','session']
    def create(self, validated_data):
        dt_sessions_data = validated_data.pop("session")
        mo = ManagedObject.objects.create(**validated_data)
        dtsession_serializer = self.fields['session']
        for dt_session_data in dt_sessions_data:
            dt_session_data['session'] = mo
            DtSession.objects.create(**dt_session_data)
       
        return mo






