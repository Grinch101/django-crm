from django.urls import path
from . import views


app_name = 'contacts'
urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('all', views.all, name='add-contact'),
    path('delete/<id>', views.delete, name='delete_contact'),
    path('update/<id>', views.update, name='update-contact'),
]
