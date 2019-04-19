import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Analytics_API.Connection.ga_custom_metrics_api import GACustomMetricsAPI

#Khởi tạo db_helper
db_controller = db_helper()

class GAHandleMetricsClientAPI(GACustomMetricsAPI):
  '''Class xử lý Goal Google Analytics API'''
  def __init__(self,request,site_id):
    GACustomMetricsAPI.__init__(self,request,site_id)

  def get_metrics_for_site(self):
    result = self.get_metrics()
    return result