from rest_framework import permissions
from rest_framework import views, status, serializers
from rest_framework.response import Response
from django.contrib.auth import login
from ..serializers import loginSerializer
from ..serializers.serializers import UserSerializer
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework import generics


User = get_user_model()
#for user in User.objects.all():
class LoginView(generics.GenericAPIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    serializer_class=loginSerializer.LoginSerializer

    def post(self, request, format=None):
        serializer = loginSerializer.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e: 
            request.data["message"]=str(e)
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
        
        user = serializer.validated_data['user']
        login(request, user, backend='..serializers.loginSerializer.MyBackend')
        resp=[]
        if(request.user.is_authenticated):
            Token.objects.get_or_create(user=user)
            resp.append(UserSerializer(user).data)
            print("hehe",request.user.is_staff)
            val=UserSerializer(user, fields=['id','username','first_name','last_name','email','last_login']).data
            val.update({"admin":request.user.is_superuser})
            val.update({"staff":request.user.is_staff})
            #resp.append(Token.objects.get_or_create(user=user)[0].__str__)
            return Response(val, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)