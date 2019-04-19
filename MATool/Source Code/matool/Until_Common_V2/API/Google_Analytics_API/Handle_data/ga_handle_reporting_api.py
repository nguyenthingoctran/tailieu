import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Analytics_API.Connection.ga_reporting_api import GAReportingAPI

#Khởi tạo db_helper
db_controller = db_helper()

class GAHandleReportingClientAPI(GAReportingAPI):
  '''Class xử lý Goal Google Analytics API'''
  def __init__(self,request,site_id):
    GAReportingAPI.__init__(self,request,site_id)

  def get_data_by_date(self,start_date, end_date):
    result = self.test_get_data_by_date(start_date, end_date)
    return result
    