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
from django.urls import path, include
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
    path('helpproviders/',HelpProviderList.as_view({'get': 'list'})),
    path('helpproviders/!<str:fonction>/',HelpProviderList.as_view({'get':'getByFunction'})),
    path('helpproviders/<int:pk>/', HelperDetail.as_view()),
    #path('message/',MessageList.as_view()),
    path('event/',EventsList.as_view()),
    path('event/<slug:convo_id>',SingleEvent.as_view()),
    path('convo/', ConvoList.as_view()),
    path('login/', LoginView.as_view()),
    path('mostate/',ManagedObjectState.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path('profile/', ProfileImage.as_view()),
    path('sites/', Sites.as_view({'get':'get_with_pagination'})),
    path('sites/all/', Sites.as_view({'get':'get_all'})),
    path('sites/lastsession/', Sites.as_view({'get':'get_last_test_per_site'})),
    path('DT_session/', SiteDT.as_view(),),
    path('groups/<int:pk>',GroupViewSet.as_view({'get': 'retrieve'})),
    path('groups/',GroupViewSet.as_view({'get': 'list'})),
    path('useringroups/',GroupViewSet.as_view({'get': 'usersInGroup'})),
    path('userinwhichgroup/<int:id>',GroupViewSet.as_view({'get': 'userinwhichgroup'})),
    path('dtsession/', DriveTestSessionViewSet.as_view({'get':'list'})),
    path('has_session/<str:site_id>',DriveTestSessionViewSet.as_view({'get':'has_session'})),
    path('dtsession/g=<int:group_id>&t=<int:technician_id>/', DriveTestSessionViewSet.as_view({'get':'dtsessionsFiltered'})),
    path('dtsession/g=<int:group_id>/',DriveTestSessionViewSet.as_view({'get':'dtsessionsFilteredByGroup'})),
    path('dtsession/', DriveTestSessionViewSet.as_view({'post':'create'})),
    path('isintimeframe/<int:id>',HelpProviderList.as_view({'get':'isTechnicianInTimeFrame'})),
    path('botmessage/',exchangeMessageRasa.as_view()),
    path('botmessageFr/',exchangeMessageRasaFrench.as_view()),
    path('stats/',DriveTestSessionViewSet.as_view({'get':'statsOnSessions'}))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
