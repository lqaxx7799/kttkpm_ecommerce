from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls.resolvers import URLPattern

#app_name = 'user'
urlpatterns = [
    path('', views.index, name='user_index'),
    path('login/', auth_views.LoginView.as_view(template_name='templates/login_form.html'), name='login'),
    path('signup/', auth_views.LoginView.as_view(template_name='templates/signup_form.html'), name='signup'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
]

