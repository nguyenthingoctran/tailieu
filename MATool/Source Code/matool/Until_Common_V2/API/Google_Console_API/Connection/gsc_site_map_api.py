import requests
import json
import urllib

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Console_API.google_console_api_auth import GSCAPIAuth

#Khởi tạo db_helper
db_controller = db_helper()
#Khởi tạo log
log = Log()

class GSCSiteMapAPI(GSCAPIAuth):
  """
  Class thực hiện các truy vấn lấy thông tin index site hoặc submit dựa vào site map
  """
  REST_URL_SITE_MAP = 'https://www.googleapis.com/webmasters/v3/sites/{0}/sitemaps/{1}?fields=contents'
  
  def __init__(self,request,site_id):
    GSCAPIAuth.__init__(self,request,site_id)

  def get_data_in_site_map(self):
    try:
      #1) HÀM MÃ HÓA urllib.parse.quote(self._gsc_site_url, safe='')
      gsc_site_url_endcode = urllib.parse.quote(self._gsc_site_url, safe='')
      url_site_map = self._gsc_site_url + 'sitemap.xml' 
      url_sitemap = urllib.parse.quote(url_site_map, safe='')
      url_site = 'https://www.googleapis.com/webmasters/v3/sites/{0}/sitemaps/{1}?fields=contents'.format(gsc_site_url_endcode,url_sitemap)
      headers = {
      'authorization': "Bearer " + self._access_token,
      "Content-Type": "application/json"
      }
      result = requests.get(url_site, headers=headers)
      return result.json()
    except Exception as inst:
      return log.write_log(inst)