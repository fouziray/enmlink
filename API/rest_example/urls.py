"""rest_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views
from restapp.views.views import *
from restapp.views.loginView import LoginView
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('reponse/<act>',Respond.as_view()),
    path('helpproviders',HelpProviderList.as_view()),
    path('helpproviders/<int:pk>/', HelperDetail.as_view()),
    #path('message/',MessageList.as_view()),
    path('event/',EventsList.as_view()),
    path('event/<slug:convo_id>',SingleEvent.as_view()),
    path('convo/', ConvoList.as_view()),
    path('login/', LoginView.as_view()),
    path('mostate/',ManagedObjectState.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('profile/', ProfileImage.as_view()),
    path('sites/', Sites.as_view()),
    path('DT_session/', SiteDT.as_view()),
    path('users_groups/',JoinUserGrpView.as_view()),
    url("", include('django_socketio.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
