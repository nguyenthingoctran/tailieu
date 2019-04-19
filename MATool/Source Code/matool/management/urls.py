from django.conf.urls import url
from django.conf.urls import url, include
from . import views

app_name = 'management'

urlpatterns = [
  
  # LOGIN/LOGOUT
  url(r'^user/ajax_login$', views.ajax_user_authenticate_login, name='ajax_user_authenticate_login'),
  url(r'^user/ajax_logout$', views.ajax_user_authenticate_logout, name='ajax_user_authenticate_logout'),
  # END LOGIN/LOGOUT

]