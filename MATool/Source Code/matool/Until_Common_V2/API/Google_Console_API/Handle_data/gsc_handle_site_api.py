import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Console_API.Connection.gsc_site_api import GSCSiteAPI

#Khởi tạo db_helper
db_controller = db_helper()

class GSCHandleSiteAPI(GSCSiteAPI):
  ''' Class xử lý GSC Search Client API '''
  def __init__(self,request,site_id):
    GSCSiteAPI.__init__(self,request,site_id)

  def get_info_site(self):
    result = self.get_sites()
    return result