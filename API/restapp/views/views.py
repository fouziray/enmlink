import json
from django.shortcuts import render

#from django.contrib.auth.models import User 
from django.http import Http404
from restapp.serializers.eventSerializer import EventSerialize
from restapp.serializers.serializers import ConvoSerializer, HelpProviderSerialize, ManagedObjectStateSerializer, ProfileSerializer, UserSerializer,SiteSerializer, TechnologySerializer , SiteSerializer2,GroupSerializer,DTSerializer
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
from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max,F,Count, ExpressionWrapper, DateTimeField,Q;
from rest_framework.pagination import LimitOffsetPagination

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
    permission_classes = (permissions.AllowAny,)
   
    
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

class HelpProviderList(ReadOnlyModelViewSet):
    
    permission_classes = (permissions.AllowAny,)
    serializer_class=HelpProviderSerialize

    
    queryset= HelpProvider.objects.all()

    def list(self, request):
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

    @action(methods=['get'],detail= True)
    def getByFunction(self,request,fonction):
        queryset= HelpProvider.objects.values('id','profile__avatar','last_login','first_name','last_name', 'fonction').filter(fonction=fonction)
        #queryset= self.get_queryset().filter(fonction=fonction)
        #serializer= HelpProviderSerialize(queryset,many=True)
        return Response(queryset)

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
            try:
                site = site_serializer.save()     
            except: 
                return Response(site_serializer.data, status=status.HTTP_302_FOUND)       
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
    
class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', ]
    pagination_class = LimitOffsetPagination
    
    def is_doctor(user):
        return user.groups.filter(name='Doctor').exists()
    def retrieve(self, request,  *args, **kwargs):
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)
    
    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    @action(detail=True)
    def usersInGroup(self,request):
            #users = User.objects.filter(groups__in=Group.objects.all().query) """It evaluates to a left join of the `restapp_user` table with `restapp_user_groups` and a simple `where` statement"""
            #users = User.objects.filter(groups__id=pk)
            #users = User.objects.filter(groups__in=Group.objects.all().query).annotate(name=Count('groups')).values('name')
            #users = User.objects.values('groups__name').annotate(total=Count('id'))
            permissionsIdsArray=[21,24,23,22] # permission related to DTsession actions
            namesGrp=User.objects.values('groups__name','groups__id','id','profile__avatar','last_login','first_name','last_name').filter(groups__name__isnull=False, groups__permissions__id=21)
            lastActivePerGroup= (namesGrp).values('groups__name').annotate(maxlast=Max('last_login'))
            return Response([namesGrp,lastActivePerGroup])
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
    def get_groups(self, request, format=None):
        group = Group.objects.first()
        group.permissions.all()
        return Response(group.data)

class DriveTestSessionViewSet(ReadOnlyModelViewSet):
    queryset = DtSession.objects.all()
    serializer_class = DTSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get', ]
    
    def retrieve(self, request,  *args, **kwargs):
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)
    
    def list(self, request):
        queryset = self.get_queryset().filter()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False)
    def dtsessionsFiltered(self,request,group_id, technician_id): # filtered using group id and technician id
            queryset = self.get_queryset().filter(Q(dtTeam=group_id) | Q(technicien=technician_id))
            serializer= self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
