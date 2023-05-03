from django.db import models

# Create your models here.
class User(models.Model):
    id= models.IntegerField
    first_name= models.CharField(max_length=100, null=True)
    last_name= models.CharField(max_length=100, null=True)
    username= models.CharField(max_length=100,null=True)
    email= models.EmailField(max_length=100,null=True)
    password= models.CharField(max_length=30, null=True)
    def __str__(self) -> str:
        return f"{id} {username} {first_name} {last_name} {email}"

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
