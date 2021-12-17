from datetime import datetime
from decimal import Context
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.serializers import Serializer
from apiRest.models import Activity, Property
from apiRest.serializers import ActivityCancelarSerializer, ActivityGetSerializers,ActivityPostSerializers, ActivityReagendarSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, time,timedelta


# Create your views here.

class Activity_APIView(APIView):
    def get(self,request,format=None,*args,**kwargs):
        hours=72
        hours_added=timedelta(hours=hours)
        weeks_added=timedelta(days=21)
        now= datetime.now()
        t1=now-hours_added
        t2= now+ weeks_added
        status=''
        activity=''
        filtroFechas=False
        if request.GET:            
            if request.GET.get('t1') and request.GET.get('t2'):
                filtroFechas=True
                t1=request.GET.get('t1',False)
                t2=request.GET.get('t2',False)
            if (request.GET.get('t1',False) and not request.GET.get('t2',False)) or ( not request.GET.get('t1',False) and request.GET.get('t2',False)):
                return Response({"mensaje":"Favor de incluir ambas fechas t1 y t2"},status=status.HTTP_400_BAD_REQUEST)
            if request.GET.get('status',False):
                status=request.GET['status']                
        
        if status=='':
            activity= Activity.objects.filter(schedule__range=[t1,t2])
        else:
            if filtroFechas: #Se enviaron las fechas en parámetros filtrar por fechas y por status 
                activity= Activity.objects.filter(status=status, schedule__range=[t1,t2])
            else:
                activity= Activity.objects.filter(status=status)

        serializer= ActivityGetSerializers(activity,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer= ActivityPostSerializers(data=request.data,context=request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Activity_Reagendar(APIView):

    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            raise Http404

    def put(self,request,pk,format=None):
        actividad= self.get_object(pk)
        serializer=ActivityReagendarSerializer(actividad,data=request.data,context={'pk':pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje":"Se han reagendado la actividad de manera correrca"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
    

class Activity_Cancelar(APIView):
    def get_object(self, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            raise Http404
    def put(self,request,pk,format=None):
        actividad=self.get_object(pk)
        serializer=ActivityCancelarSerializer(actividad,data=request.data,context={'pk':pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje":"se ha actualizado el status de la actividad"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        
        
