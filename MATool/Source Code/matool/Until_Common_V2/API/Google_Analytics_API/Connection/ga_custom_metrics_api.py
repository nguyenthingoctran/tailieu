import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Analytics_API.google_analytics_API_auth import GAAPIAuth

#Khởi tạo db_helper
db_controller = db_helper()

class GACustomMetricsAPI(GAAPIAuth):
  """
  Class thực hiện các truy vấn liên quan đến metric
  """
  # GOAL
  REST_URL_GET_LIST     = 'https://www.googleapis.com/analytics/v3/management/accounts/{0}/webproperties/{1}/customMetrics'    #account_id, property_id
  REST_URL_GET = ''
  REST_URL_UPDATE = ''
  REST_URL_INSERT = ''
  REST_URL_DELETE = ''
  # END GOAL

  def __init__(self,request,site_id):
    GAAPIAuth.__init__(self,request,site_id)

  def get_metrics(self):
    try:
      headers = {'authorization': "Bearer " + self._access_token}
      url = self.REST_URL_GET_LIST.format(self._account_id, self._property_id, self._view_id)
      result = requests.get(url, headers=headers)
      return result.json()   
    except Exception as inst:
      return Log().write_log(inst)