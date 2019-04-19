import datetime as DT

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from pprint import pprint

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Custom_Search_API.Handle_data.gcs_handle_check_rank_api import HandleCheckRankAPI

# Create your views here.

#Khởi tạo db_helper
db_controller = db_helper()
#Khởi tạo log
log = Log()

def test(request):
  try: 

    #1) list_api free dùng để test
    list_api = ['AIzaSyDR0eKPkAtjNSfLBHj3aD5DXubxTexODDA','AIzaSyCrLVyFvNqD7l4zITgRaG2_R8CJyLiaSps','AIzaSyA0qSK2G6tQh1ygj-ydACwpZE89L7g-FcQ','AIzaSyDywPE47EjcVb8Y58yD8jhPSY7pZkuj1FA','AIzaSyBzD7t8pKnMTE-Hazi81zqpnbJeyV52274','AIzaSyDEgd5Rlwoyh3S2ssqDSPhpWozl_6VoOuc','AIzaSyCKTUT5TRdYXHsXr8Cjo3-YaLr-42oC6Qg','AIzaSyCjteDrcxv2Tf5S2aHdNSfgBFpeHsLfijA','AIzaSyBOQH0nftg-fTWst35ZrhGVtHA6bv6CH48']
    #1.1) biến để thay đổi api
    api_change = 0
    #1.2) biến tính số lượt đã query của api
    api_query_count = 0
    #1.3) biến tính max số lượt query
    api_query_total = 70
    #1.4) biến lấy ngày check
    today = DT.datetime.today()
    check_date = str(today)
    #2) lấy tổng keyword id thuộc site_id =3 
    site_id = 3
    sql_query_list_keyword_id = '''SELECT id FROM dev_matool_db.ranking_keyword where site_id = {0} and not keyword = "" '''.format(site_id)
    object_list_keyword_id = db_controller.query(sql_query_list_keyword_id)
    #2.1) lưu id vào list
    list_keyword_id = []
    for kw in object_list_keyword_id:
      list_keyword_id.append(kw['id'])

    for kw_id in list_keyword_id: 
      print(api_query_count) 
      if api_query_count >= api_query_total:
        api_change += 1
      
      api_key =  list_api[api_change]
      print('api_key:  %s' %api_key)
      dict_data = HandleCheckRankAPI(api_key).get_rank_keyword_checked_in_site(kw_id)
      pprint(dict_data)
      api_query_count += 3
      #2.2) các biến để lưu vào database
      keyword_id = dict_data['id']
      url_rank = dict_data['url_rank']
      position = dict_data['position']
      site_id = dict_data['site_id']
      #2.2.1) gọi biến prev_1, pre_v2, prev_3 gán giá trị cho nhau
      sql_query_update_prev = '''SELECT * FROM dev_matool_db.ranking_keyword WHERE id = {0}'''.format(keyword_id)
      object_update_prev = db_controller.query(sql_query_update_prev)
      #2.2.2) biến prev_1
      prev_rank_1 = object_update_prev[0]['prev_rank_1']
      prev_rank_2 = object_update_prev[0]['prev_rank_2']
      prev_rank_3 = object_update_prev[0]['prev_rank_3']
      top_rank = object_update_prev[0]['top_rank']
      #2.2.3) Trước khi lưu giá trị cần gán lại giá trị của các biến
      #2.2.4) Nếu giá trị = None thì đổi qua -1
      if prev_rank_1 is None:
        prev_rank_1 = -1
      if prev_rank_2 is None:
        prev_rank_2 = -1
      if prev_rank_3 is None:
        prev_rank_3 = -1 
      #2.2.5) Giá trị rank 3 lần check gần nhất: 
      prev_rank_3 = prev_rank_2
      prev_rank_2 = prev_rank_1
      prev_rank_1 = position

      #2.2.6) Vị trí rank cao nhất của từ khóa đạt được
      if top_rank is None or top_rank == -1:
        top_rank = position
      else:
        if top_rank <= position:
          top_rank = position
        else:
          top_rank = top_rank


      #2.3) lưu dữ liệu vào rank session
      sql_insert_rank_session = '''INSERT INTO dev_matool_db.ranking_session 
                                        (position,url_rank,checked_date,keyword_id,site_id)
                                        VALUE({0},'{1}','{2}',{3},{4})'''.format(position,url_rank,check_date,
                                                                        keyword_id,site_id)
      print('lưu rank session')
      db_controller.execute(sql_insert_rank_session)
      #2.4) update dữ liệu ranking_keyword
      sql_update_ranking_keyword = '''UPDATE dev_matool_db.ranking_keyword
                                    SET prev_rank_1= {0},prev_rank_2= {1},prev_rank_3= {2},current_url_rank = '{3}',top_rank= {4}
                                    WHERE id = {5}'''.format(prev_rank_1,prev_rank_2,prev_rank_3,url_rank,top_rank,keyword_id)
      db_controller.execute(sql_update_ranking_keyword)
      print('update ok')

  except Exception as inst:
    return log.write_log(inst)    
  return HttpResponse() 

def ranking_index(request):
  return render(request, 'apps/ranking/ranking_index.html')