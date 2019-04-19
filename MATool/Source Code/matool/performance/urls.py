from django.conf.urls import url
from django.conf.urls import url, include
from . import views

app_name = 'performance'

urlpatterns = [
  #===============================================
  #============== Test ===========================
  #===============================================
  url(r'^test$', views.test, name='test'),    
  url(r'^test2$', views.test2, name='test2'),    
  url(r'^test3$', views.test3, name='test2'),    

  #===============================================
  #============== Blog ===========================
  #===============================================
  url(r'^blog$', views.blog_index, name='blog_index'),    
  url(r'^blog/(?P<id>\d+)$', views.blog_detail, name='blog_detail'),     
  url(r'^blog/ajax-get-data-tab-overview$', views.ajax_blog_get_data_tab_overview, name='ajax_blog_get_data_tab_overview'),     
  url(r'^blog/ajax-get-data-tab-ranking$', views.ajax_blog_get_data_tab_ranking, name='ajax_blog_get_data_tab_ranking'),     
]