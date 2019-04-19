import os
import sys
import requests
import urllib
import datetime
import logging
import json
from django.http import HttpResponse

from management.models import site_user_auth
from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log

#Khởi tạo db_helper
db_controller = db_helper()
#Khởi tạo log
log = Log()

# Google Custome Search Config (QuyetDV)
CX_CLIENT_ID = '010439002756461283328:eyacu8irct8'
API_KEY = 'AIzaSyDywPE47EjcVb8Y58yD8jhPSY7pZkuj1FA'

class GCSCheckRankAPI:
  ' Class này dùng để lấy dữ liệu rank của keyword sau khi check trên google'
  
  _cx_client_id = ''
  _api_key = ''

  def __init__(self,api_key):
    self._cx_client_id = CX_CLIENT_ID
    self._api_key = api_key

  def check_rank_keyword_api(self,keyword,location='jp',start=1):
    #1) Url để check rank
    api_key = self._api_key
    cx_client_id = self._cx_client_id
    url = 'https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&gl=%s&num=10&start=%d' % (api_key,cx_client_id,keyword,location,start)

    #2) dữ liệu trả về
    response = requests.get(url).json() 
    
    return response
    