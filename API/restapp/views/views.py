import json
from django.shortcuts import render

#from django.contrib.auth.models import User 
from django.http import Http404
from restapp.serializers.eventSerializer import EventSerialize
from restapp.serializers.serializers import ConvoSerializer, HelpProviderSerialize, ManagedObjectStateSerializer, ProfileSerializer, UserSerializer,SiteSerializer, TechnologySerializer , SiteSerializer2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from restapp.models import HelpProvider, Convo, Profile# Message
from restapp.modelEvent import Events
from restapp.models import User, ManagedObject, Technology, DtSession
from rest_framework.decorators import api_view
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import UpdateProfileForm
class UserList(APIView):
   
    def get(self, request, format=None):
         users = User.objects.all()
         serializer = UserSerializer(users, many=True)
         return Response(serializer.data)

    def post(self, request, format=None):
         serializer = UserSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
         user = self.get_object(pk)
         user.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetail(APIView):
     """
     Retrieve, update or delete a user instance.
     """
     def get_object(self, pk):
         try:
             return User.objects.get(pk=pk)
         except User.DoesNotExist:
             raise Http404

     def get(self, request, pk, format=None):
         user = self.get_object(pk)
         user = UserSerializer(user)
         return Response(user.data)

     def put(self, request, pk, format=None):
         user = self.get_object(pk)
         serializer = UserSerializer(user, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     def delete(self, request, pk, format=None):
         user = self.get_object(pk)
         user.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

class Respond(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, act):
        return Response("this is "+str(act))

class HelperDetail(APIView):
    def get_object(self, pk):
         try:
             return HelpProvider.objects.get(pk=pk)
         except HelpProvider.DoesNotExist:
             raise Http404

    def get(self, request, pk, format=None):
         user = self.get_object(pk)
         user = HelpProviderSerialize(user)
         return Response(user.data)

    def put(self, request, pk, format=None):
         user = self.get_object(pk)
         serializer = HelpProviderSerialize(user, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
         user = self.get_object(pk)
         user.delete()
         
         
         return Response(status=status.HTTP_204_NO_CONTENT)

class HelpProviderList(APIView):
    def get(self, request, format=None):
         users = HelpProvider.objects.all()
         serializer = HelpProviderSerialize(users, many=True)
         return Response(serializer.data)

    def post(self, request, format=None):
         serializer = HelpProviderSerialize(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
         user = self.get_object(pk)
         user.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

class ConvoList(APIView):
    def get(self, request, format=None):
         users = Convo.objects.all()
         serializer = ConvoSerializer(users, many=True)
         return Response(serializer.data)

    def post(self, request, format=None):
         serializer = ConvoSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
         user = self.get_object(pk)
         user.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
from django.db import connection
from django.http import JsonResponse
"""class MessageList(APIView):
    def get(self, request, format=None):
         users = Message.objects.all()
         serializer = MessageSerializer(users, many=True)
         return Response(serializer.data)

    def post(self, request, format=None):
         serializer = MessageSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
         user = self.get_object(pk)
         user.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
"""
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class EventsList(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format=None):
         users = Events.objects.distinct('type_name')
         serializer = EventSerialize(users, many=True)
         #query="SELECT data :: json -> 'event' AS value FROM events "
         #return self.rawsql(query) # using 
         return Response(serializer.data)
    
    def rawsql(self,query):
        with connection.cursor() as cursor:
             cursor.execute(query)
             results= cursor.fetchall()
        return JsonResponse(results,safe=False)
class SingleEvent(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = (permissions.AllowAny,)
    def get(self, request, convo_id ):
        events=Events.objects.filter(sender_id=convo_id).exclude(type_name="action")
        serialized_events= EventSerialize(events,many=True)
        return Response(serialized_events.data)

class ManagedObjectState(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
         serializer = ManagedObjectStateSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileImage(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    """def post(self,request, format=None):
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return Response( {'profile_form': '1'},status=status.HTTP_201_CREATED)
        else:
            return Response( {'profile_form': ''},status=status.HTTP_201_CREATED)"""
    @api_view(['POST'])
    def post(self, request, format=None):
        try:
            # exist then update
            profile = Profile.objects.get(user=request.user)
            print(request.user)
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            # not exist then create
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response('user doesnt have a profile')

class Sites(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    def get(self, request, format=None):
         #Technologies= Technology.objects.all()
         #finaltech = TechnologySerializer(Technologies,many=True)
         #MosTechnologies = ManagedObject.objects.prefetch_related('managedObject').all()
         MosTechnologies= ManagedObject.objects.all()
         #MosTechnologies= ManagedObject.objects.select_related('managedObject').all()
         serializer = SiteSerializer(MosTechnologies, many=True)
         return Response(serializer.data)
    def post(self, request, format=None):
         site_serializer = SiteSerializer(data=request.data)
         if (site_serializer.is_valid(raise_exception=True)):
            site = site_serializer.save()            
            return Response(site_serializer.data, status=status.HTTP_201_CREATED)
         return Response(site_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """def post(self, request, format=None):
         serializer = ConvoSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
         user = self.get_object(pk)
         user.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)"""
    

class SiteDT(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    def get(self, request, format=None):
        # DT = DtSession.objects.all()
        # serializer = DTSerializer(DT, many=True)
        # return Response(serializer.data)
        MosDTSession= ManagedObject.objects.all()
        #MosTechnologies= ManagedObject.objects.select_related('managedObject').all()
        serializer = SiteSerializer2(MosDTSession, many=True)
        return Response(serializer.data)



