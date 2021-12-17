"""TrueHomeTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from apiRest.views import Activity_APIView, Activity_Cancelar,  Activity_Reagendar, Property_APIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('v1/activities/reagendar/(?P<pk>\d+)', Activity_Reagendar.as_view(),name="reagendar"),    
    url('v1/activities/cancelar/(?P<pk>\d+)', Activity_Cancelar.as_view(),name="reagendar"),    
    url('v1/activities',Activity_APIView.as_view(),name="listar"),
    url('v1/properties',Property_APIView.as_view(),name="listarP")

    

]
