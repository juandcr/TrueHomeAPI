
from rest_framework import serializers
from apiRest.models import Activity, Property, Survey
from datetime import datetime, time,timedelta


class PropertySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Property
        fields=['pk','title','address','description','status']

class SurveySerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model= Survey
        fields=['pk']

class ActivityGetSerializers(serializers.ModelSerializer):
    
    condition=serializers.CharField()    
    property= PropertySerializer( source="property_id")
    survey= SurveySerializer(read_only=True)


    class Meta:
        model = Activity
        fields=['pk','schedule','title','created_at_datetime','status','condition','property','survey']
        #fields = '__all__'
            
    
class ActivityPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Activity        
        fields=['pk','property_id','schedule','title','created_at_datetime','updated_at_datetime','status']
    
    def validate_property_id(self,value):        
        propiedad=Property.objects.filter(pk=value.pk,status='activo').first()
        if not propiedad:
            mensaje='La propiedad con id: '+str(value.pk)+ ' no está activa y no se pueden crear actividades para la misma'
            raise serializers.ValidationError(mensaje)
        return value

    def validate_schedule(self,value):         
        hours=1
        hours_added=timedelta(hours=hours)
        t2=value+hours_added        
        actividad=Activity.objects.filter(property_id=self.context['property_id'],schedule__range=[value,t2])
        if actividad:
            mensaje='ya existe una actividad programada para este horario para la propiedad: '+ str(self.context['property_id'])
            raise serializers.ValidationError(mensaje)
        return value
        
    def create(self, validated_data):
        return Activity.objects.create(**validated_data)        

class ActivityReagendarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity     
        fields=['schedule']

    def validate_schedule(self,value):         
        hours=1
        hours_added=timedelta(hours=hours)
        t2=value+hours_added
        actividad_a_actualizar=self.instance
        actividad_existente=Activity.objects.filter(property_id=actividad_a_actualizar.property_id,schedule__range=(value,t2))
        if actividad_existente:
            if actividad_existente=='cancelada':
                mensaje='No se puede reagendar actividades canceladas'
            else:   
                mensaje='ya existe una actividad programada para este horario para la propiedad: '+ str(actividad_a_actualizar.property_id.pk)
            raise serializers.ValidationError(mensaje)
        return value

class ActivityCancelarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity        
        fields=['status']

    def validate_status(self,value):
        if value!="cancelada":
            mensaje='Solo se puede cambiar el status de la actividad a "cancelada"'
            raise serializers.ValidationError(mensaje)
        return value
