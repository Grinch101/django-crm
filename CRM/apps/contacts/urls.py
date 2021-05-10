from django.urls import path
from . import views


app_name = 'contacts'
urlpatterns = [
    path('add', views.add, name='add'),
    path('all', views.all, name='add-contact'),
    path('delete/<contact_id>', views.delete, name='delete-contact'),
    path('update/<contact_id>', views.update, name='update-contact'),
]
