import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Analytics_API.google_analytics_API_auth import GAAPIAuth
from Until_Common_V2.API.Google_Analytics_API.Connection.ga_account_api import GAAccountAPI

#Khởi tạo db_helper
db_controller = db_helper()

class GAHandleAccountAPI(GAAccountAPI):
  ''' Class xử lý GA Account Client'''
  def __init__(self,request,site_id):
    GAAccountAPI.__init__(self,request,site_id)

  def get_account_id_for_site(self):
    result = self.get_accounts()
    return result


