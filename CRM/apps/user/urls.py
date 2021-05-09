from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('current_user', views.current_user, name='current_user'),
    path('user_update', views.user_update, name='user_update'),

]
