import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Console_API.Connection.gsc_search_analytics_api import GSCSearchAnalyticsAPI

#Khởi tạo db_helper
db_controller = db_helper()

class GSCHandleSearchAnalyticsAPI(GSCSearchAnalyticsAPI):
  ''' Class xử lý GSC Search Client API '''
  def __init__(self,request,site_id):
    GSCSearchAnalyticsAPI.__init__(self,request,site_id)

  #LẤY TOP TỪ KHÓA THEO URL TRONG GSC
  #Chỉ được chọn 1 trong 3 cái clicks,position,impressions
  def get_keywords_in_top_for_url(self, start_date, end_date, url,top,clicks = False,position = False,impressions = False):
    try:
      #1) dữ liệu trả về từ GSC
      dict_result = self.get_keywords_by_url( start_date, end_date, url)

      #1.1) sắp xếp lại dữ liệu  trả về theo lựa chọn
      #1.1.1) Click: lượt click của từ khóa
      #1.1.2) Position: vị trí trung bình trên tìm kiếm của google
      #1.1.3) impressions: Số lần hiển thị trên google
      list_keyword = dict_result['rows']
      if clicks == True:
        sort_funtion = lambda x : x['clicks']
      elif position == True:
        sort_funtion = lambda x : x['position']
      elif impressions == True:
        sort_funtion = lambda x : x['impressions']

      list_keyword.sort(key=sort_funtion)

      #2)Phân tích dữ liệu
      #2.1)check số lượng lấy ra
      count = 0
      #2.2) danh sách top keyword trả về
      #2.3) Dữ liệu trả về có dạng : {'clicks': 11.0,
      #                                'ctr': 0.6111111111111112,
      #                               'impressions': 18.0,
      #                                'keys': ['データ 分類 手法'],
      #                                'position': 1.9444444444444444} 
      list_keyword_top = []
      for data in list_keyword:
        count += 1
        list_keyword_top.append(data)
        if count == top:
          break

      return list_keyword_top
    except Exception as inst:
      return Log().write_log(inst)  
