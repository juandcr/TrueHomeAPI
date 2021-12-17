# TrueHomeAPI
API  REST for TrueHome tecnhical test 
pip install -r requirements.txt
python manage.py migrate (ya se tienen las migraciones en el repo, no es necesario realizar un makemigrations)
python manage.py runserver

se necesita tener una instalación de postgresql local 
cambiar usuario y contraseña en el settings.py

parametros url:
t1= fecha inicial para el filtro de fechas
t2= fecha final
status= estado de la actividad

endpoints:
"v1/activities/reagendar/:Activityid"
    PUT: Permite reagendar una actividad, se pasa el parametro schedule por body:
        {
        
        "schedule": "2021-12-28T22:44"
     
        }

"v1/activities/cancelar/:Activityid'"
    PUT: permite cancelar una actividad, se pasa el nuevo status, solo permite cancelar
    {
        
        "status": "cancelada"
     
    }


"v1/activities"
    POST: Creación de actividad
    {
        "property_id": 1,
        "schedule": "2021-12-25T22:44",
        "title": "ActividadPostmanORM2",        
        "status": "cancelada"
    }
    GET: puede incluir los parametros url mencionados anteriormente para filtrar las actividades o usar el filtro default solicitado en caso de no tener filtros

"v1/properties"
    POST: creación de propiedad:
    {
        "title": "Propiedad3",
        "address": "Descripción",
        "description": "Descripcion",
        "status": "activo"
    }

    GET: muestra todas las propiedades 
