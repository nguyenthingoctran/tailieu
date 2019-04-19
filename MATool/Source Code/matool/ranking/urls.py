from django.conf.urls import url
from django.conf.urls import url, include
from . import views

app_name = 'ranking'

urlpatterns = [
  url(r'^test$', views.test, name='test'),
  url(r'^$', views.ranking_index, name='ranking_index'),
]