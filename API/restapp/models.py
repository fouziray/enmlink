from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User ,AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
    #    date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user
class User(AbstractBaseUser, PermissionsMixin):
    from restapp.models import UserManager
    use_in_migrations = True
    #REQUIRED_FIELDS = ('user',)
    #user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    id= models.IntegerField
    first_name= models.CharField(max_length=100, null=True)
    last_name= models.CharField(max_length=100, null=True)
    username= models.CharField(max_length=100,null=True, unique=True)
    email= models.EmailField(max_length=100,null=True, unique=True)
    password= models.CharField(max_length=100, null=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    is_staff= models.BooleanField(default=False)
    is_active= models.BooleanField(default=False)
    objects = UserManager()
    def __str__(self) -> str:
        return f"{self.id} {self.username} {self.first_name} {self.last_name} {self.email}"

  




class HelpProvider(User):
    fonction=models.CharField(max_length=20, null=False)

class Convo(models.Model):
#   speaker = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='speaker')
#   user_id= models.ForeignKey(HelpProvider,on_delete=models.DO_NOTHING, related_name='user_id')
    user_id=models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    def __str__(self):
        return self.user.username
"""class Message(models.Model):
    convo_id= models.ForeignKey(Convo, on_delete=models.CASCADE, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
   # intent = models.ForeignKey(Intent,on_delete=models.DO_NOTHING)
    text=models.CharField(max_length=100, null=True)
    user_id= models.ForeignKey(User,on_delete=models.DO_NOTHING)
    source_is_user= models.BooleanField(default=True)   
"""
#class Intent(models.Model):
#    intent = models.CharField(max_length=30,default="")
#    message_id = models.ForeignKey(Message, on_delete= models.CASCADE)
     
#class entity(models.Model):
#    intent_id = models.ForeignKey(Intent, on_delete=models.CASCADE)
#    name = models.CharField(max_length=20, null=False)
    
class Connexion(models.Model):
    help_provider=models.ForeignKey(HelpProvider,on_delete=models.DO_NOTHING, related_name='help_provider')
    created=models.DateTimeField(auto_now_add=True)
    convo_id=models.ForeignKey(Convo, on_delete=models.CASCADE)

class ManagedObject(models.Model):
    site_id = models.CharField(max_length=7, primary_key=True)
    wilaya=models.CharField(max_length=100,null=True)
    UOP_CHOICES = (
        ('EAST', 'EAST'),
        ('CENTER', 'CENTER'),
        ('SOUTH', 'SOUTH'),
    )
    UOP=models.CharField(max_length=6,null=True,choices=UOP_CHOICES)

class Technology(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    #auto_increment_id=models.IntegerField(primary_key=True)
    managedObject=models.ForeignKey(ManagedObject,on_delete=models.DO_NOTHING, related_name='managedObject')
    TYPE_CHOICES = (
        ('3G', '3G'),
        ('4G', '4G'),
        ('2G', '2G'),
    )
    STATE_CHOICES = (
        ('ACTIVE', 'ACTIVE'),
        ('LOCKED', 'LOCKED'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    state= models.CharField(max_length=6,null=True,choices=STATE_CHOICES)
    throughput= models.IntegerField
from django.contrib.auth.models import Group

class DtSession(models.Model):
    site=models.ForeignKey(ManagedObject,on_delete=models.DO_NOTHING)
    dtTeam=models.ForeignKey(Group,on_delete=models.DO_NOTHING)
    #technicianTeam=models.ForeignKey(Group,on_delete=models.DO_NOTHING)
    technicien=models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_time=models.DateTimeField()
    end_Time=models.DateTimeField()
    # don't forget develop socket io django + rabbitmq
