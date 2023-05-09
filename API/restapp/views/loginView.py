from rest_framework import permissions
from rest_framework import views, status, serializers
from rest_framework.response import Response
from django.contrib.auth import login
from ..serializers import loginSerializer

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = loginSerializer.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e: 
            request.data["message"]=str(e)
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)
        
        user = serializer.validated_data['user']
        login(request, user)
        if(request.user.is_authenticated):
       
            return Response(request.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)