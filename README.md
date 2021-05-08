# django-crm

from django.urls import path
from . import views


app_name = 'activity'
urlpatterns = [
    path('<contact_id>', views.activity, name='all activities'),
    path('<contact_id>', views.activity, name='add activities'),
    path('<contact_id>/delete/<activity_id>',
         views.delete_activity, name='delete-activity'),
]



from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

# Create your views here.


@require_GET
def activity(req, contact_id):
    return JsonResponse(data=f'all activities using GET for {contact_id}', status=200, safe=False)


@require_POST
def activity(req, contact_id):
    return JsonResponse(data=f'add page for activity to contact {contact_id}', status=201, safe=False)


@require_http_methods(['DELETE'])
def del_activity(req, contact_id, activity_id):
    return JsonResponse(data=f'delete {activity_id} from contact {contact_id}', status=200, safe=False)
