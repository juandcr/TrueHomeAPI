from django.contrib import admin

from apiRest.models import Activity, Property, Survey

# Register your models here.
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display=('title','created_at_datetime','updated_at_datetime')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display=('title','created_at_datetime','updated_at_datetime')

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display=('get_activity',)

    def get_activity(self,obj):
        return obj.activity_id.title

    get_activity.short_description='Encuesta'    