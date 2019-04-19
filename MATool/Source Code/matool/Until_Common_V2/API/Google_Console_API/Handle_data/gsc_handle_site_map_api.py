import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Console_API.Connection.gsc_site_map_api import GSCSiteMapAPI

#Khởi tạo db_helper
db_controller = db_helper()

class GSCHandleSiteMapAPI(GSCSiteMapAPI):
  ''' Class xử lý GSC Search Client API '''
  def __init__(self,request,site_id):
    GSCSiteMapAPI.__init__(self,request,site_id)

  def get_index_for_site(self):
    #1) lấy dữ liệu Json của site map
    result = self.get_data_in_site_map()

    value_index_site_map = 0
    #1.1) lấy giá trị index của site
    for i in result['contents']:
      if i['type'] == 'web':
        value_index_site_map = int(i['indexed'])

    return value_index_site_map