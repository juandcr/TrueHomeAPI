from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.fields.related import OneToOneField
from datetime import datetime, tzinfo    
import pytz



# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255,null=False, blank=False,verbose_name="título")
    address = models.TextField(null=False, blank=False,verbose_name="dirección")
    description = models.TextField(null=False, blank=False,verbose_name="descripción")
    created_at_datetime= models.DateTimeField(null=False,blank=False, verbose_name="Fecha de creación",auto_created=True)
    updated_at_datetime= models.DateTimeField(null=False,blank=False, verbose_name="Fecha de actualización",auto_now=True)
    disabled_at_datetime= models.DateTimeField(null=True,blank=True, verbose_name="Fecha de deshabilitación")
    status= models.CharField(max_length=35,null=False,blank=False, verbose_name="estado",choices=(('activo','Activo'),('inactivo','Inactivo')))

    class Meta:
        verbose_name="Propiedad"
        verbose_name_plural="Propiedades"
        ordering=['-created_at_datetime']

    def __str__(self):
        return self.title
    
class Activity(models.Model):
    property_id= models.ForeignKey(Property,verbose_name="propiedad",on_delete=models.CASCADE)
    schedule= models.DateTimeField(null=False,blank=False, verbose_name="Horario")
    title = models.CharField(max_length=255,null=False, blank=False,verbose_name="título")
    created_at_datetime= models.DateTimeField(null=False,blank=False, verbose_name="Fecha de creación",default=datetime.now)
    updated_at_datetime= models.DateTimeField(null=False,blank=False, verbose_name="Fecha de actualización",auto_now=True)
    status= models.CharField(max_length=35,null=False,blank=False, verbose_name="estado",choices=(('activo','Activo'),('cancelada','Cancelada'),('done','realizada')),default="activo")

    class Meta:
        verbose_name="Actividad"
        verbose_name_plural="Actividades"
        ordering=['-created_at_datetime']

    def __str__(self):
        return self.title

    def condition(self):
        now=datetime.now()
        utc=pytz.UTC
        if self.status=="activo" and  self.schedule.replace(tzinfo=utc)>now.replace(tzinfo=utc):
            return "Pendiente a realizar"
        if self.status=="activo" and  self.schedule.replace(tzinfo=utc)<now.replace(tzinfo=utc):
            return "Atrasada"
        if self.status=="done" and  self.schedule.replace(tzinfo=utc)>now.replace(tzinfo=utc):
            return "Finalizada"
        return self.title
    

class Survey(models.Model):
    activity_id= OneToOneField(Activity,on_delete=models.CASCADE, verbose_name="actividad")
    answers= JSONField()
    created_at_datetime= models.DateTimeField(null=False,blank=False, verbose_name="Fecha de creación")

    class Meta:
        verbose_name="Encuesta"
        verbose_name_plural="Encuestas"
        ordering=['-created_at_datetime']

    def __str__(self):
        return str(self.activity_id.title)