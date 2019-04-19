import json

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from pprint import pprint
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

from performance.report_blog_post import export_report_blog_post,download_data_for_report_blog_post,get_data_to_report_blog_post
from Until_Common_V2.API.Google_Custom_Search_API.Handle_data.gcs_handle_check_rank_api import HandleCheckRankAPI
from Until_Common_V2.API.Hubspot_API.Handle_data.hubspot_handle_analytics_API import HubspotHandleAnalayticsAPI
from Until_Common_V2.log import Log  
from Until_Common_V2.db_helper import db_helper  
from Until_Common_V2.enum import AjaxResponseResult, LoginStatus

#==================================================================================
db_controller = db_helper()
#==================================================================================
# Create your views here.
def test(request):
  start = datetime.now()
  # download_data_for_report_blog_post.download_blog_post_info()

  # download_data_for_report_blog_post.download_blog_post_data()

  # response = export_report_blog_post.export_sessions_report_blog_posts_xlsx('text_blog_post.xlsx',11,'2018-01-01','2019-03-01')
  response = export_report_blog_post.export_keyword_report_blog_posts_xlsx('text_blog_post.xlsx',11,'2018-01-01','2019-03-01')
  
  print("Total time:",datetime.now() - start)

  return response 
  # return HttpResponse() 

def test2(request):
  # api_key = 'AIzaSyCjteDrcxv2Tf5S2aHdNSfgBFpeHsLfijA'
  # check_rank_api = HandleCheckRankAPI(api_key)
  # # result = check_rank_api.get_rank_keyword_checked_in_site(35)
  # result = check_rank_api.check_rank_keyword_api('ストレージ スナップ ショット',)
  
  # f = open('Check_keyword.txt',"w")
  # json.dump(result,f)
  # f.close()
  return HttpResponse()
  
def test3(request):
  list_data = get_data_to_report_blog_post.get_keyword_blog_post_from_DB(11,'2018-01-01','2019-03-01')

  pprint(list_data)
  return HttpResponse()

def blog_index(request):
  # Get list site
  sql_query_list_site_info = '''SELECT p.id,p.name,p.logo
                    FROM management_site p
                    ORDER BY id ASC
                  '''
  object_list_site_info = db_controller.query(sql_query_list_site_info)

  data = { 
    'list_site_info' : object_list_site_info, 
    'page_url' : 'performance/blog/site' 
  }
  return render(request, 'apps/performance/blog_index.html', data)  

def blog_detail(request, id):
  #1. Get list site info
  sql_query_list_site = '''SELECT id,name
                    FROM management_site
                    ORDER BY id ASC
                  '''
  object_list_site_info_select = db_controller.query(sql_query_list_site)

  #1.1 Thêm all site
  list_site_info = [{'id':0,"name":"All Page"}]
  list_site_info.extend(object_list_site_info_select)

  #2. Get Site info
  id = int(id)
  if id != 0 :
    #1. Get Site info
    sql_query_site_info = '''SELECT *
                    FROM management_site
                    WHERE id={0}
                    '''.format(id)
    object_site_info = db_controller.query(sql_query_site_info)
    site_info = object_site_info[0]
  elif id == 0:
    site_info = {'id' : 0,"name" : "All Site"}

  # Get all user
  sql_query_user_info = '''
                    SELECT * FROM auth_user;
                  '''
  object_user_info = db_controller.query(sql_query_user_info)

  #4. Truyền data lên template tùy theo trường hợp đã auth hay chưa

  data = { 
    'site_info' : site_info, 
    'list_site_info' : list_site_info, 
    'user_info' : object_user_info,
    'page_url' : '/performance/blog/site'
  }
  return render(request, 'apps/performance/blog_detail.html', data)

def ajax_blog_get_data_tab_overview(request):
  if request.method == 'POST':

    if request.is_ajax():
      result = AjaxResponseResult.success.value
      try:
        # 1) Lấy dữ liệu từ request
        param_site_id = int(request.POST['site_id'])

        # 1.1)Các biến cần dùng trong hàm
        number_of_month_get_value = 3
        today = datetime.now()

        #1.2)Lấy tháng ngay phía trước tháng hiện tại bây giờ đang là 2019-04-20 thì lấy 2019-03-01
        last_month = datetime(today.year,today.month,1)
        last_month = last_month - timedelta(1)
        last_month = datetime(last_month.year,last_month.month,1)

        #2)Đưa ra cái list ngày trong data_table
        list_month_get_value = []
        for i in range(number_of_month_get_value-1,-1,-1):
          date = last_month - relativedelta(months=i)
          list_month_get_value.append(date.strftime('%Y-%m-%d'))

        #2.1)Lấy ngày bắt đầu và kết thúc để lấy dữ liệu từ DB
        start_date = list_month_get_value[0]
        end_date = list_month_get_value[-1]

        #2.2)Lấy dữ liệu từ DB
        dict_data_table = get_data_to_report_blog_post.get_sessions_blog_post_from_DB(param_site_id,start_date,end_date)
        for index,data in enumerate(dict_data_table['CTA Click Rate']):
          data = round(data*100,2)
          dict_data_table['CTA Click Rate'][index] = str(data) + '%'

        #2.3)Đổi định dạng kiểu dữ liệu
        number_of_blog = len(dict_data_table['Title'])

        #2.4)Lấy dữ liệu trong ruột của data table ra để đổi thành dạng xuất được trong jinja
        value_in_data_table = dict_data_table.values()
        list_data_table = []
        for i in range(number_of_blog):
          list_term = []
          for data in value_in_data_table:
            list_term.append(data[i])
          list_data_table.append(list_term)  

        #3)Xuất dữ liệu ra view
        data = {
                'list_month_get_value' : list_month_get_value,
                'list_data_table' : list_data_table,
                }
        return render(request, 'apps/performance/blog/data_tab_overview.html',data)
      except Exception as inst:
        result = Log().write_log(inst)
        return HttpResponse(result)
        
    return HttpResponse('')

def ajax_blog_get_data_tab_ranking(request):
  if request.method == 'POST':
    if request.is_ajax():
      result = AjaxResponseResult.success.value
      try:
        # 1) Lấy dữ liệu từ request
        param_site_id = int(request.POST['site_id'])

        # 1.1)Các biến cần dùng trong hàm
        number_of_month_get_value = 3
        today = datetime.now()

        #1.2)Lấy tháng ngay phía trước tháng hiện tại bây giờ đang là 2019-04-20 thì lấy 2019-03-01
        last_month = datetime(today.year,today.month,1)
        last_month = last_month - timedelta(1)
        last_month = datetime(last_month.year,last_month.month,1)

        #2)Đưa ra cái list ngày trong data_table
        list_month_get_value = []
        for i in range(number_of_month_get_value-1,-1,-1):
          date = last_month - relativedelta(months=i)
          list_month_get_value.append(date.strftime('%Y-%m-%d'))

        #2.1)Lấy ngày bắt đầu và kết thúc để lấy dữ liệu từ DB
        start_date = list_month_get_value[0]
        end_date = list_month_get_value[-1]

        #2.2)Lấy dữ liệu từ DB
        dict_data_table = get_data_to_report_blog_post.get_keyword_blog_post_from_DB(param_site_id,start_date,end_date)

        #2.3)Đổi định dạng kiểu dữ liệu
        number_of_blog = len(dict_data_table['Title'])

        #2.4)Lấy dữ liệu trong ruột của data table ra để đổi thành dạng xuất được trong jinja
        value_in_data_table = dict_data_table.values()
        list_data_table = []
        for i in range(number_of_blog):
          list_term = []
          for data in value_in_data_table:
            list_term.append(data[i])
          list_data_table.append(list_term)  

        #3)Xuất dữ liệu ra view
        data = {
                'list_month_get_value' : list_month_get_value,
                'list_data_table' : list_data_table,
                }

        return render(request, 'apps/performance/blog/data_tab_ranking.html',data)
      except Exception as inst:
        result = Log().write_log(inst)
        return HttpResponse(result)
        
    return HttpResponse('')
