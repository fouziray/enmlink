from django.db import models

# Create your models here.
class User(models.Model):
    id: models.IntegerField
    first_name: models.CharField(max_length=100)
    last_name: models.CharField(max_length=100)
    username: models.CharField(max_length=100)
    email: models.EmailField(max_length=100)
    def __str__(self) -> str:
        return f"{id} {username} {first_name} {last_name} {email}"