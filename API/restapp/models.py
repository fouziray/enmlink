from django.db import models
from django.contrib.auth.models import User ,AbstractUser, AbstractBaseUser, PermissionsMixin
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    #REQUIRED_FIELDS = ('user',)
    #user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    id= models.IntegerField
    first_name= models.CharField(max_length=100, null=True)
    last_name= models.CharField(max_length=100, null=True)
    username= models.CharField(max_length=100,null=True, unique=True)
    email= models.EmailField(max_length=100,null=True, unique=True)
    password= models.CharField(max_length=30, null=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return f"{self.id} {self.username} {self.first_name} {self.last_name} {self.email}"


class HelpProvider(User):
    fonction=models.CharField(max_length=20, null=False)

class Convo(models.Model):
#   speaker = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='speaker')
#   user_id= models.ForeignKey(HelpProvider,on_delete=models.DO_NOTHING, related_name='user_id')
    user_id=models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')

class Message(models.Model):
    convo_id= models.ForeignKey(Convo, on_delete=models.CASCADE, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
   # intent = models.ForeignKey(Intent,on_delete=models.DO_NOTHING)
    text=models.CharField(max_length=100, null=True)
    user_id= models.ForeignKey(User,on_delete=models.DO_NOTHING)
    source_is_user= models.BooleanField(default=True)   

class Intent(models.Model):
    intent = models.CharField(max_length=30,default="")
    message_id = models.ForeignKey(Message, on_delete= models.CASCADE)
     
class entity(models.Model):
    intent_id = models.ForeignKey(Intent, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False)
    
class Connexion(models.Model):
    help_provider=models.ForeignKey(HelpProvider,on_delete=models.DO_NOTHING, related_name='help_provider')
    created=models.DateTimeField(auto_now_add=True)
    convo_id=models.ForeignKey(Convo, on_delete=models.CASCADE)
