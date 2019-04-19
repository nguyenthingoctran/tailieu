import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Analytics_API.google_analytics_API_auth import GAAPIAuth

#Khởi tạo db_helper
db_controller = db_helper()

class GAAccountAPI(GAAPIAuth):
  """
  Class thực hiện các truy vấn đến account GA được cấp quyền cho user authent access token
  """
  # ACCOUNT
  REST_URL_GET_LIST     = 'https://www.googleapis.com/analytics/v3/management/accounts'
  REST_URL_GET_PROPERTY = 'https://www.googleapis.com/analytics/v3/management/accounts/{0}/webproperties'                 #account_id
  REST_URL_GET_VIEW     = 'https://www.googleapis.com/analytics/v3/management/accounts/{0}/webproperties/{1}/profiles'    #account_id, property_id
  # END ACCOUNT

  def __init__(self,request,site_id):
    GAAPIAuth.__init__(self,request,site_id)

  def get_accounts(self):
    headers = {'authorization': "Bearer " + self._access_token}
    url = self.REST_URL_GET_LIST
    result = requests.get(url, headers=headers)
    return result.json()

  def get_properties(self):
    headers = {'authorization': "Bearer " + self._access_token}
    url = self.REST_URL_GET_PROPERTY.format(self._account_id)
    result = requests.get(url, headers=headers)
    return result.json()

  def get_views(self):
    headers = {'authorization': "Bearer " + self._access_token}
    url = self.REST_URL_GET_VIEW.format(self._account_id, self._property_id)
    result = requests.get(url, headers=headers)
    return result.json()