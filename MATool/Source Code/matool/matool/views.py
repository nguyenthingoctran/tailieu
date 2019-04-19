from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from Until_Common_V2.db_helper import db_helper

# Get an instance of a db_helper
db_controller = db_helper()

# Index Page
def index(request):
  return render(request, 'index.html')

# Get list site
def ajax_get_list_site(request):
    if request.method == 'POST':
        if request.is_ajax():
            detail_url = request.POST['detail_url']
            detail_all_url = request.POST['detail_all_url']
            sql_query_list_site_info = '''SELECT p.id,p.name,p.logo
                      FROM management_site p
                      ORDER BY id ASC
                    '''
            object_list_site_info = db_controller.query(sql_query_list_site_info)

            data = { 
                'detail_url' : detail_url, 
                'detail_all_url' : detail_all_url,
                'list_site_info' : object_list_site_info
            }
            return render(request, 'control/global/list_site.html', data)