from django.urls import path
from . import views


app_name = 'activity'
urlpatterns = [
    path('<contact_id>', views.activity.as_view(), name='activities'),
    path('<contact_id>/delete/<activity_id>',
         views.delete_activity, name='delete-activity'),
]
