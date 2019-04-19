import requests
import json
import pprint
import urllib

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Console_API.google_console_api_auth import GSCAPIAuth

#Khởi tạo db_helper
db_controller = db_helper()

class GSCSearchAnalyticsAPI(GSCAPIAuth):
  """
  Class thực hiện các truy vấn đến search analytics được cấp quyền cho user authent access token
  """
  REST_URL_QUERY = 'https://www.googleapis.com/webmasters/v3/sites/{0}/searchAnalytics/query'   #site_url

  def __init__(self,request,site_id):
    GSCAPIAuth.__init__(self,request,site_id)

  def get_keywords_by_url(self, start_date, end_date, url):
    try:
      data = {
          "startDate": start_date,
          "endDate": end_date,
          "dimensions": ["query"],
          "dimensionFilterGroups" : [
              {
                  "filters" : [
                          {
                          "dimension": "page",
                          "operator": "equals",
                          "expression": url
                      }
                  ],
              }
          ],
          "aggregationType": "byPage",
          "searchType": "web",
          "rowLimit": 30
      }

      gsc_site_url_endcode = urllib.parse.quote(self._gsc_site_url, safe='')
      rest_url = self.REST_URL_QUERY.format(gsc_site_url_endcode)

      headers = {
      'authorization': "Bearer " + self._access_token,
      "Content-Type": "application/json"
      }

      result = requests.post(rest_url, data=json.dumps(data), headers=headers)
      
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)  
  
  # lấy tất cả keyword trong site trong thời gian lựa chọn
  def get_all_keyword_in_site(self, start_date, end_date):
    try:
      data = {
          "startDate": start_date,
          "endDate": end_date,
          "dimensions": ["query"],
          "searchType": "web",
          "responseAggregationType": "auto"
      }

      gsc_site_url_endcode = urllib.parse.quote(self._gsc_site_url, safe='')
      rest_url = self.REST_URL_QUERY.format(gsc_site_url_endcode)

      headers = {
      'authorization': "Bearer " + self._access_token,
      "Content-Type": "application/json"
      }
      result = requests.post(rest_url, data=json.dumps(data), headers=headers)
      return result.json() 
    except Exception as inst:
      return Log().write_log(inst)

  #Lấy tất cả page trong site trong thời gian lựa chọn
  def get_all_page_in_site(self, start_date, end_date):
    try:
      data = {
          "startDate": start_date,
          "endDate": end_date,
          "dimensions": ["page"],
          "searchType": "web",

      }

      gsc_site_url_endcode = urllib.parse.quote(self._gsc_site_url, safe='')
      rest_url = self.REST_URL_QUERY.format(gsc_site_url_endcode)

      headers = {
      'authorization': "Bearer " + self._access_token,
      "Content-Type": "application/json"
      }
      result = requests.post(rest_url, data=json.dumps(data), headers=headers)
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)