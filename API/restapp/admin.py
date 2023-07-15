from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import User, ManagedObject, Technology


admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Technology)
admin.site.register(ManagedObject)
