import datetime
from datetime import timedelta
import json
from django.shortcuts import render

#from django.contrib.auth.models import User 
from django.http import Http404
from restapp.serializers.eventSerializer import EventSerialize
from restapp.serializers.serializers import ConvoSerializer, HelpProviderSerialize, ManagedObjectStateSerializer, ProfileSerializer, UserSerializer,SiteSerializer, TechnologySerializer , SiteSerializer2,GroupSerializer,DTSerializer, DTserializercreation, MessageRasaBotSerializer, SessionExtensionSerializer
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
from django.utils.timezone import now
from rest_framework import pagination
from rest_framework import generics

async_mode = None
import os
from django.http import HttpResponse
import socketio
import requests
basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode='eventlet')
thread = None

# Tracks the total number of users using the admin channel
num_users = 0

# Maximum number of members in a group
threshold = 4
@sio.on('connection-bind')
def connection_bind(sid, data):
    pass
@sio.on('disconnect')
def test_disconnect(sid):
    pass
class exchangeMessageRasa(generics.GenericAPIView):
        permission_classes = (permissions.AllowAny,)
        serializer_class=MessageRasaBotSerializer
        queryset=Events.objects
        def post(self, request, format=None):
            api_url="http://localhost:5005/webhooks/rest/webhook"
            serializer = MessageRasaBotSerializer(data=request.data)
            if serializer.is_valid():
                headers =  {"Content-Type":"application/json"}
                try:
                    response=requests.post(api_url, data=json.dumps(serializer.data),headers=headers)
                except NameError:  
                    print("hhh"+str(NameError))
                    return Response(str(NameError))
                return Response(response.json(), status=response.status_code)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class exchangeMessageRasaFrench(generics.GenericAPIView):
        serializer_class=MessageRasaBotSerializer
        queryset=Events.objects
        permission_classes = (permissions.AllowAny,)
        def post(self, request, format=None):
            api_url="http://localhost:5005/webhooks/rest/webhook"
            serializer = MessageRasaBotSerializer(data=request.data)
            if serializer.is_valid():
                headers =  {"Content-Type":"application/json"}
                response=requests.post(api_url, data=json.dumps(serializer.data),headers=headers)
                return Response(response.json(), status=response.status_code)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class=UserSerializer
    queryset=User.objects.all()
#    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request, format=None):
         users = User.objects.all()
         serializer = UserSerializer(users, many=True,fields=['id','username','first_name','last_name','email','last_login'])
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
    
    def put(self, request, format=None):
        userdata=request.data
        print(str(userdata)+"hehhheeeeeeeeeeeeeeee");
        serializer=UserSerializer(User.objects.get(pk=userdata['id']),data=userdata)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
    
class UserDetail(generics.GenericAPIView):
     """
     Retrieve, update or delete a user instance.
     """
     serializer_class=UserSerializer
     queryset=User.objects
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
    swagger_schema = None
    permission_classes = (permissions.AllowAny,)

    def get(self, request, act):
        return Response("this is "+str(act))

class HelperDetail(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
   
    serializer_class=HelpProviderSerialize
    queryset=HelpProvider.objects.all()
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
    @action(methods=['get'], detail=True)
    def isTechnicianInTimeFrame(self, request, id):
        val=now()
        queryset=DtSession.objects.filter(technicien=id,start_time__lte=val,end_Time__gte=val).exists()
        
        return Response(DtSession.objects.filter(technicien=id,start_time__lte=val,end_Time__gte=val).values_list("id",flat=True),status=status.HTTP_200_OK)
        

class ConvoList(APIView):
    swagger_schema = None
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
class EventsList(generics.GenericAPIView):
    serializer_class=EventSerialize
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = (permissions.AllowAny,)
    queryset=Events.objects.all()
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
class SingleEvent(generics.GenericAPIView):
    serializer_class=EventSerialize
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = (permissions.AllowAny,)
    queryset=Events.objects
    def get(self, request, convo_id ):
        events=Events.objects.filter(sender_id=convo_id).exclude(Q(action_name="action_listen") | Q(action_name="action_session_start")).order_by("timestamp")

        serialized_events= EventSerialize(events,many=True)
        return Response(serialized_events.data)

class ManagedObjectState(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = (permissions.AllowAny,)
    swagger_schema = None

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
        except :
            parameter=request.POST.get("id",None)
            # not exist then create
            if(parameter != None):
                profile = User.objects.get(id=parameter)
            else:
                profile = User.objects.get(id=request.user.id)

            
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=profile)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        try:
            parameter=request.GET.get("id",None)
            if(parameter != None):
                profile = Profile.objects.get(user=parameter)
            else:
                profile = Profile.objects.get(user=request.user.id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"avatar":"/static/default.jpg"},status = status.HTTP_204_NO_CONTENT)
   

class ExamplePagination(pagination.PageNumberPagination):       
       page_size = 6
class Sites(ModelViewSet, LimitOffsetPagination):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    serializer_class=SiteSerializer
    
    queryset=ManagedObject.objects.all()
    pagination_class= ExamplePagination

    @action(detail=True, methods=['get'])
    def get_last_test_per_site(self,request,format=None):
        last=DtSession.objects.values('site').annotate(max=Max('end_Time'))
        return Response(last)


    @action(detail=True, methods=['get'])
    def get_all(self,request,format=None):
         MosTechnologies= ManagedObject.objects.all()
         serializer = SiteSerializer(MosTechnologies, many=True)
         return Response(serializer.data)
    @action(detail=True, methods=['get'])       
    def get_with_pagination(self, request, format=None):
         #Technologies= Technology.objects.all()
         #finaltech = TechnologySerializer(Technologies,many=True)
         #MosTechnologies = ManagedObject.objects.prefetch_related('managedObject').all()
         MosTechnologies= ManagedObject.objects.all()
         result=self.paginate_queryset(MosTechnologies)
         serializer = SiteSerializer(result, many=True) 
         return self.get_paginated_response(serializer.data)
  
#         serializer = SiteSerializer(MosTechnologies, many=True)
#         return Response(serializer.data)
    
    @action(detail=True, methods=['get'])       
    def search_with_pagination(self, request, format=None):
         request = self.request
         query = request.GET.get('q', None)
         #Technologies= Technology.objects.all()
         #finaltech = TechnologySerializer(Technologies,many=True)
         #MosTechnologies = ManagedObject.objects.prefetch_related('managedObject').all()
         MosTechnologies= ManagedObject.objects.filter(Q(wilaya__icontains=query) |
                         Q(site_id__icontains=query) |
                         Q(UOP__icontains=query)
                        )
         result=self.paginate_queryset(MosTechnologies)
         serializer = SiteSerializer(result, many=True) 
         return self.get_paginated_response(serializer.data)

    
    def post(self, request, format=None):
         site_serializer = SiteSerializer(data=request.data,many=True)
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
    @action(detail=True)
    def userinwhichgroup(self,request,id):
        return Response(User.objects.values('groups__id').filter(id=id))
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
        
class DriveTestSessionViewSet(ModelViewSet):
    queryset = DtSession.objects.all().order_by('-start_time')
    serializer_class = DTSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ["get","post"]    
    def getsingle(self, request,pk=None):
        queryset = DtSession.objects.all()
        single=get_object_or_404(queryset,pk=pk)
        # query = request.GET.get('query', None)  # read extra data
        return Response(self.serializer_class(single).data,
                        status=status.HTTP_200_OK)

    def list(self, request):
        queryset = self.get_queryset().filter()
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False)
    def dtsessionsFilteredByGroup(self,request,group_id): # filtered using group id and technician id
            queryset = self.get_queryset().filter(dtTeam=group_id)
            serializer= self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def dtsessionsFilteredBytechnician(self,request,technician_id): # filtered using group id and technician id
            queryset = self.get_queryset().filter(technicien=technician_id)
            serializer= self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def dtsessionsFiltered(self,request,group_id, technician_id): # filtered using group id and technician id
            queryset = self.get_queryset().filter(Q(dtTeam=group_id) & Q(technicien=technician_id))
            serializer= self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False)
    def statsOnSessions(self,request): # filtered using group id and technician id
            queryset = DtSession.objects.values("site__UOP").annotate(number=Count("site__UOP"))
            BeforeLastWeek= DtSession.objects.values("start_time","end_Time").filter(start_time__gte=now().date()-datetime.timedelta(14),end_Time__lte=now().date()-datetime.timedelta(7)).count()
            LastWeek= DtSession.objects.values("start_time","end_Time").filter(start_time__gte=now().date()-datetime.timedelta(7),end_Time__lte=now().date()).count()
            current= DtSession.objects.filter(start_time__lte=now(),end_Time__gte=now())
            serializer= self.get_serializer(current, many=True)
            taskprogress= DtSession.objects.order_by().values("site").distinct().count()
            numberofsites= ManagedObject.objects.count()
            if(BeforeLastWeek==0):
                BeforeLastWeek=1
            if(numberofsites==0):
                numberofsites=1
            return Response({"lastweek":LastWeek,"percentage":LastWeek*100/BeforeLastWeek,"testsPerUOP":queryset,"currentSessions":serializer.data, "taskProgress": (taskprogress/numberofsites)*100}, status=status.HTTP_200_OK)
    
    @action(detail=False)
    def has_session(self,request,site_id):
        queryset=self.get_queryset().filter(site=site_id,start_time__gte=now().date()).exists()
        return Response(queryset, status=status.HTTP_200_OK)
    def create(self, request):
        serializer = DTserializercreation(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def todays_sessions(self,request):
        queryset=self.get_queryset().filter(start_time__gte=now()- datetime.timedelta(hours=12),start_time__lte=now()+datetime.timedelta(hours=12))
        serializer= self.get_serializer(queryset, many=True)
        newdict=serializer.data
        if serializer.data:
            newdict=[]
            for i in range(len(serializer.data)):
                print("_______________"+str(serializer.data[i]["technicien"]["id"]))
                try:
                    profile = Profile.objects.get(user=serializer.data[i]["technicien"]["id"])
                    newdict1 = ProfileSerializer(profile).data        
                    newdict1.update(serializer.data[i])
                    newdict.append(newdict1)
                except:
                    newdict1={"avatar":"/static/default.jpg"}
                    newdict1.update(serializer.data[i])
                    newdict.append(newdict1)
                    print("exception no profile found")

      

      
        return Response(newdict, status=status.HTTP_200_OK)
    
    
    def post(self, request, format=None):
        serializer = DTserializercreation(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def extend_session(self,request):
        serializer = SessionExtensionSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            # ob=DtSession.objects.get(id=serializer.data["session_id"]).update(end_Time=F("start_time")+ timedelta(minutes=serializer.data["time"]))

            ob=DtSession.objects.get(id=serializer.data["session_id"])
            updatedDsessionserial=DTserializercreation(ob)
            ob=updatedDsessionserial.data
            currentdatetime=datetime.strptime(ob["endDate"], '%Y-%m-%dT%H:%M:%SZ')            
            print(str(currentdatetime))

            ob.update({"endDate": currentdatetime+timedelta(minutes=serializer.data["time"]) })
            updatedDsessionserial=DTserializercreation(data=ob)
            if updatedDsessionserial.is_valid(raise_exception=True):
                updatedDsessionserial.save()
                print("validdddd")
                DtSession.objects.filter(pk=ob["id"]).update(end_Time=currentdatetime+timedelta(minutes=serializer.data["time"]))

            return Response(ob, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinUserGrpView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]

   
   
    def get(self, request, *args, **kwargs):
        # join query users and groups
        sql_query = """
            SELECT restapp_user.id , restapp_user.username , restapp_user.email , restapp_user_groups.id 
            FROM  restapp_user
            INNER JOIN restapp_user_groups ON restapp_user.id = restapp_user_groups.user_id
        """

        # SQL query execution with Django's connection
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        # json data response
        data = []
        for row in result:
            item = {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'group_id': row[3],
                
            }
            data.append(item)

        return Response(data)





