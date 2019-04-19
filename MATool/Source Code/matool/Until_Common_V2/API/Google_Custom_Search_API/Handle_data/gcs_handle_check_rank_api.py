import requests
import json
from pprint import pprint

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Custom_Search_API.Connection.gcs_check_rank_api import GCSCheckRankAPI

#Khởi tạo db_helper
db_controller = db_helper()
#Khởi tạo log
log = Log()

class HandleCheckRankAPI(GCSCheckRankAPI):
  
  def __init__(self,api_key):
    GCSCheckRankAPI.__init__(self,api_key)

  def get_rank_keyword_checked_in_site(self,id_keyword):
    try:
      #1) dict dữ liệu trả về
      #1.1)Format : {
      #             'id': id_keyword,
      #             'url_rank' : link top 
      #             'position' : vị trí
      #             'site_id' : id của site
      #             }
      dict_result = {}
      #1.1.1) index_page
      sql_query_keyword_info = '''SELECT * FROM ranking_keyword WHERE id = {0}'''.format(id_keyword)
      object_keyword_info = db_controller.query(sql_query_keyword_info)
      #1.2) Lấy các biến trong db cần để check
      #1.2.1) Keyword Name
      keyword_name = object_keyword_info[0]['keyword']
      #1.2.5) site id
      site_id = object_keyword_info[0]['site_id']
      #1.2.2) kiểm tra xem đã có thứ hạng chưa
      prev_rank_1 = object_keyword_info[0]['prev_rank_1']
      #1.2.3) Vị trí check từ khóa: mặc định là jp
      location = object_keyword_info[0]['location']
      #1.2.4) url check
      current_target_url = object_keyword_info[0]['current_target_url']
      #1.2.5) url site
      sql_query_site_info = '''SELECT url FROM dev_matool_db.management_site where id = {0}'''.format(site_id)
      object_site_info = db_controller.query(sql_query_site_info)
      url_site = object_site_info[0]['url']
      if current_target_url != '-1' and current_target_url != None:
        check_domain = current_target_url
      else:
        check_domain = url_site
      if keyword_name != '' and keyword_name != None:
        #1.2) check index page: nếu start tăng lên thì số lượt check sẽ giảm :
        if prev_rank_1 != None or prev_rank_1 != -1:
          #1.2.1) Biến này check lại rank cũ trước khi check lượt mới
          check_prev_rank_1 = prev_rank_1 / 10
          #1.3.1)nếu từ khóa trong top  <= 10 , ưu tiên quét từ trang đầu tiên
          if check_prev_rank_1 <= 1:
            check_index_page = 0
          #1.3.2) nếu từ khóa trong khoảng từ 11 đến 20 , bắt đầu check trang thứ 2
          elif 1 < check_prev_rank_1 <= 2:
            check_index_page = 1
          #1.3.3) Nếu từ khóa trong khoảng 21 - 30 thì check từ trang thứ 3  
          else :
            check_index_page = 2
        else:
          check_index_page = 0

        #1.4) list index để check thứ tự
        list_index = [0,1,2]
        #1.4.1) bỏ vị trí ưu tiên ra khỏi list index
        list_index.pop(check_index_page)
        #1.4.2) chèn vị trí ưu tiên check lên đầu mảng, để giảm lượng query
        list_index.insert(0,check_index_page)
        
        #2) tiến hành check rank cho keyword
        for i in list_index:

          #2.1) biến check xem có tìm thấy từ khóa trong 30 kết quả đầu tiên không
          is_found = False
          #2.1.1) start : trang bắt đầu lấy kết quả
          start = 10 * i + 1

          #2.1.2) kết quả trả về
          response = self.check_rank_keyword_api(keyword_name,location,start)
          list_items = response['items']
          for j in range(10):
            #2.2.2) Link kết quả tìm kiểm trả về
            url_items = list_items[j]['link']
            #2.2.3) Vị trí của từ khóa
            position = j + start
            #2.2.4) kiểm tra url link có domain trong đó không
            if check_domain in url_items:
              #2.2.5) Tạo dict để lưu dữ liệu check được
              dict_result['id'] = id_keyword
              dict_result['url_rank'] = url_items
              dict_result['position'] = position
              dict_result['site_id'] = site_id
              #2.2.6) Tìm thấy kết quả thì thoát vòng lặp tìm check từ khác
              is_found = True
              break
            else:
              #2.3) Nếu không có thứ hạng thì lưu lại keyword, position = -1, url có hai trường hợp
              dict_result['id'] = id_keyword
              #2.3.1) TH1 : check url chính xác của blog - thì lưu lại url của blog
              if check_domain == current_target_url:
                dict_result['url_rank'] = current_target_url
              #2.3.2) TH2: Check theo domain của Site thì trả về giá trị: ''  
              elif check_domain == url_site:
                dict_result['url_rank'] = ''

              dict_result['position'] = -1
              dict_result['site_id'] = site_id

          if(is_found == True):
            break
     
      return dict_result
    except Exception as inst:
      return log.write_log(inst)

              


