import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Console_API.google_console_api_auth import GSCAPIAuth

#Khởi tạo db_helper
db_controller = db_helper()
#Khởi tạo log
log = Log()

class GSCSiteAPI(GSCAPIAuth):
  """
  Class thực hiện các truy vấn đến account GSC được cấp quyền cho user authent access token
  """
  def __init__(self,request,site_id):
    GSCAPIAuth.__init__(self,request,site_id)

  def get_sites(self):
    try:
      headers = {'authorization': "Bearer " + self._access_token}
      url = 'https://www.googleapis.com/webmasters/v3/sites'
      result = requests.get(url, headers=headers)
      return result.json()
    except Exception as inst:
      return log.write_log(inst)