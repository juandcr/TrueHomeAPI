from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.fields.related import OneToOneField


# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255,null=False, blank=False,verbose_name="título")
    address = models.TextField(null=False, blank=False,verbose_name="dirección")
    description = models.TextField(null=False, blank=False,verbose_name="descripción")
    created_at_datetime= models.DateField(null=False,blank=False, verbose_name="Fecha de creación")
    updated_at_datetime= models.DateField(null=False,blank=False, verbose_name="Fecha de actualización")
    disabled_at_datetime= models.DateField(null=True,blank=True, verbose_name="Fecha de deshabilitación")
    status= models.CharField(max_length=35,null=False,blank=False, verbose_name="estado",choices=(('activo','Activo'),('inactivo','Inactivo')))

    class Meta:
        verbose_name="Propiedad"
        verbose_name_plural="Propiedades"
        ordering=['-created_at_datetime']

    def __str__(self):
        return self.title
    
class Activity(models.Model):
    property_id= models.ForeignKey(Property,verbose_name="propiedad",on_delete=models.CASCADE)
    schedule= models.DateField(null=False,blank=False, verbose_name="Horario")
    title = models.CharField(max_length=255,null=False, blank=False,verbose_name="título")
    created_at_datetime= models.DateField(null=False,blank=False, verbose_name="Fecha de creación")
    updated_at_datetime= models.DateField(null=False,blank=False, verbose_name="Fecha de actualización")
    status= models.CharField(max_length=35,null=False,blank=False, verbose_name="estado",choices=(('activo','Activo'),('inactivo','Inactivo')))

    class Meta:
        verbose_name="Actividad"
        verbose_name_plural="Actividades"
        ordering=['-created_at_datetime']

    def __str__(self):
        return self.title
    

class Survey(models.Model):
    activity_id= OneToOneField(Activity,on_delete=models.CASCADE, verbose_name="actividad")
    answers= JSONField()
    created_at_datetime= models.DateField(null=False,blank=False, verbose_name="Fecha de creación")

    class Meta:
        verbose_name="Encuesta"
        verbose_name_plural="Encuestas"
        ordering=['-created_at_datetime']

    def __str__(self):
        return str(self.activity_id.title)