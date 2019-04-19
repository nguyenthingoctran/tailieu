"""
hubspot auth api
"""
import json
import urllib
import requests
import os
import sys
import logging
import datetime

from django.http import HttpResponse
from django.conf import settings
from management.models import site_user_auth  

# Get an instance of a logger
logger = logging.getLogger(__name__)

BASE_OAUTH_AUTHORIZE_URL    = "https://app.hubspot.com/oauth/480402/authorize"
BASE_OAUTH_GET_ACCESS_TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"
BASE_OAUTH_GET_ACCESS_TOKEN_INFO_URL = "https://api.hubapi.com/oauth/v1/access-tokens"

AUTH_STATE_SESSION_NOT_EXISTS = '-1'
AUTH_STATE_EXPRIESED = '0'
AUTH_STATE_AUTHETICATED = '1'

class HubspotAPIAuth:

  _client_id = ''
  _client_secret = ''
  _access_code = ''
  _redirect_uri = ''
  _access_token = ''

  def __init__(self,site_id ,request = None,access_code = '', redirect_uri = ''):
    self._client_id = settings.HUBSPOT_OAUTH_CLIENT_ID
    self._client_secret = settings.HUBSPOT_OAUTH_CLIENT_SECRET
    self._access_code = access_code
    self._redirect_uri = redirect_uri

    #Nếu không truyền vào request thì tự động hiểu là đang chạy schedule
    if request != None:
      print("Lấy access token bình thường")
      self._access_token = self.get_last_access_token(request,site_id)
    else:
      print("Lấy access token cho Schudule")
      self._access_token = self.get_last_access_token_schedule(site_id)

  def call_api_get_access_token_info(self, access_token):
    url = BASE_OAUTH_GET_ACCESS_TOKEN_INFO_URL + '/' + access_token
    result = requests.get(url)

    return result.json()

  def call_api_get_refresh_access_token(self, refresh_token):
    params = {
      'grant_type': 'refresh_token',
      'client_id': self._client_id,
      'client_secret': self._client_secret,
      'redirect_uri': self._redirect_uri,
      'refresh_token': refresh_token
    }
    data = urllib.parse.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    result = requests.post(
      BASE_OAUTH_GET_ACCESS_TOKEN_URL,
      data,
      headers
    )
    
    return result.json()

  def call_api_get_access_token(self):
    params = {
      'grant_type': 'authorization_code',
      'client_id': self._client_id,
      'client_secret': self._client_secret,
      'redirect_uri': self._redirect_uri,
      'code': self._access_code
    }
    data = urllib.parse.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    result = requests.post(
      BASE_OAUTH_GET_ACCESS_TOKEN_URL,
      data,
      headers
    )
    
    return result.json()

  def get_authenticate_state(self, request, site_id):
    try:
      current_user_id = str(request.user.id)
      #1. Khởi tạo tên session lưu access token, refresh token theo site
      access_token = ''
      refresh_token = ''
      expires_in = datetime.datetime.now()
      time_now = datetime.datetime.now()
      is_exists_db = False
      is_exists_session = False

      session_key_access_token = "hb_access_token_" + str(site_id) + "_" + current_user_id
      session_key_refresh_token = "hb_refresh_token_" + str(site_id) + "_" + current_user_id
      session_key_expires_in = "hb_expires_in_" + str(site_id) + "_" + current_user_id

      #1.1 Lưu giá trị trạng thái auth mặc định là chưa tồn tại trong session
      authenticate_state = AUTH_STATE_SESSION_NOT_EXISTS
      
      #2 Lấy thông tin access token, refresh token
      #2.1 Trường hợp đã có token lưu trong session
      if request.session.get(session_key_access_token) and request.session.get(session_key_refresh_token):
        print('#2.1 Trường hợp đã có token lưu trong session')
        access_token = request.session.get(session_key_access_token)
        refresh_token = request.session.get(session_key_refresh_token)
        str_expires_in = request.session.get(session_key_expires_in)
        expires_in = datetime.datetime.strptime(str_expires_in, '%Y-%m-%d %H:%M:%S.%f')
        is_exists_session = True

      #2.2 Trường hợp chưa có token lưu trong session
      if not is_exists_session:
        print('#2.2 Trường hợp chưa có token lưu trong session -> Lấy từ DB')
        site_user_auth_info = site_user_auth.objects.filter(user_id=request.user.id, site_id=site_id).first()
        if site_user_auth_info and site_user_auth_info.last_refresh_token != '':
          expires_in = time_now + datetime.timedelta(minutes=330) #5.5 hours
          access_token = site_user_auth_info.last_access_token
          refresh_token = site_user_auth_info.last_refresh_token
          is_exists_db = True

      #3 Check expires nếu tồn tại giá trị trong session
      if is_exists_db or is_exists_session :
        print('#3 Check expires nếu tồn tại giá trị trong session/db')
        #3.1 Kiểm tra xem access token còn thời gian không
        is_expires = True

        #3.2 Gán trạng thái Auth -> expires
        authenticate_state = AUTH_STATE_EXPRIESED

        if access_token != '':
          print('-- Get Auth info with access code = ' + access_token)
          if time_now < expires_in and not is_exists_db:
            print('--#3.3 Check is not is_expries')
            is_expires = False
          print('time_now: ' + str(time_now))
          print('expires_in: ' + str(expires_in))
        if not is_expires:
          print('#3 not is_expires')
          authenticate_state = AUTH_STATE_AUTHETICATED
          if not is_exists_session:
            request.session[session_key_access_token] = access_token
            request.session[session_key_refresh_token] = refresh_token
            request.session[session_key_expires_in] = expires_in.strftime('%Y-%m-%d %H:%M:%S.%f')
            print('#3 update session')
          
      print('===== authenticate_state : ' + str(authenticate_state))
      return authenticate_state
    except Exception as inst:
      #2. Lấy thông tin chi tiết lỗi (Msg, File name, Line number)
      exc_type, ms_tb, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      exc_msg = 'File : {0} | Line : {1} | Type : {2}\nError: {3}'.format(fname, exc_tb.tb_lineno,exc_type,ms_tb)
      
      #3. Lưu vào file erro.log
      logger.error('Exception : ' + str(type(inst)))
      logger.error(exc_msg)

      #4. In ra màn hình console
      print(exc_msg)

  def get_last_access_token(self, request, site_id):
    try:
      current_user_id = str(request.user.id)
      #print('get_last_access_token (user_id:' + current_user_id + ', site_id:' + str(site_id) + ')')

      #1. Khởi tạo tên session lưu access token, refresh token theo site
      access_token = ''
      refresh_token = ''
      expires_in = datetime.datetime.now()
      time_now = datetime.datetime.now()
      is_need_refresh_token = False
      is_need_create_token = False

      session_key_access_token = "hb_access_token_" + str(site_id) + "_" + current_user_id
      session_key_refresh_token = "hb_refresh_token_" + str(site_id) + "_" + current_user_id
      session_key_expires_in = "hb_expires_in_" + str(site_id) + "_" + current_user_id
      
      #2 Lấy thông tin access token, refresh token
      #2.1 Trường hợp đã có token lưu trong session
      if request.session.get(session_key_access_token) and request.session.get(session_key_refresh_token):
        print("%50s %20s"%('#2.1 Trường hợp đã có token lưu trong session','site_id :' + str(site_id)))
        access_token = request.session.get(session_key_access_token)
        refresh_token = request.session.get(session_key_refresh_token)
        str_expires_in = request.session.get(session_key_expires_in)
        expires_in = datetime.datetime.strptime(str_expires_in, '%Y-%m-%d %H:%M:%S.%f')

        #2.1.1 Trường hợp access token đã hết hạn -> Refresh token
        if time_now >= expires_in:
          is_need_refresh_token = True

      else:
        print("%50s %20s"%('#2.2 Trường hợp chưa có trong session -> Lấy từ DB','site_id :' + str(site_id)))
        #2.2 Trường hợp chưa có trong session -> Lấy từ DB
        site_user_auth_info = site_user_auth.objects.filter(user_id=request.user.id, site_id=site_id).first()

        #2.2.1 TH đã có trong DB
        if site_user_auth_info and site_user_auth_info.last_refresh_token != '':
          print('#2.2.1 TH đã có trong DB -> Refresh token')
          is_need_refresh_token = True
        else:
          #2.2.2 TH không có trong DB
          print('#2.2.2 TH không có trong DB')
          is_need_create_token = True

      #3 Check expires nếu tồn tại giá trị trong session hoặc DB
      if is_need_create_token or is_need_refresh_token :
        #.3.1 Refresh current token
        if is_need_refresh_token :
          #3.1.1 Get site auth info
          site_user_auth_info = site_user_auth.objects.filter(user_id=request.user.id, site_id=site_id).first()
          refresh_token = site_user_auth_info.last_refresh_token

          print('#3.1.2 Refresh new access token from refresh token')
          #3.1.2 Refresh new access token from refresh token
          refresh_access_token_info = self.call_api_get_refresh_access_token(refresh_token)
          access_token = refresh_access_token_info['access_token']
        #3.2 Create a new token
        else :
            #3.2.1 Create new site auth
            if not site_user_auth_info:                
              site_user_auth_info = site_user_auth()

            print(' #3.2.2 Create new access token')
            #3.2.2 Create new access token
            new_access_token_info = self.call_api_get_access_token()
            access_token = new_access_token_info.get('access_token')
            refresh_token = new_access_token_info.get('refresh_token')

        #3.3 Get new session time
        expires_in = time_now + datetime.timedelta(minutes=330) #5.5 hours

        #3.2 Update/Create DB
        site_user_auth_info.last_refresh_token = refresh_token
        site_user_auth_info.site_id = site_id
        site_user_auth_info.save()
    
        #3.3 Update session
        request.session[session_key_access_token] = access_token
        request.session[session_key_refresh_token] = refresh_token
        request.session[session_key_expires_in] = expires_in.strftime('%Y-%m-%d %H:%M:%S.%f')
        # Trả về giá trị access token 
      return access_token
    except Exception as inst:
      #2. Lấy thông tin chi tiết lỗi (Msg, File name, Line number)
      exc_type, ms_tb, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      exc_msg = 'File : {0} | Line : {1} | Type : {2}\nError: {3}'.format(fname, exc_tb.tb_lineno,exc_type,ms_tb)
      
      #3. Lưu vào file erro.log
      logger.error('Exception : ' + str(type(inst)))
      logger.error(exc_msg)

      #4. In ra màn hình console
      print(exc_msg)

  # Hàm xử lý authen cho schedule 
  # (Lấy theo user id = admin -> ĐK bắt buộc user admin phải authen tất cả các site)
  def get_last_access_token_schedule(self, site_id):
    try:
      current_user_id = 2 #Schedule task user

      #1. Khởi tạo tên session lưu access token, refresh token theo site
      access_token = ''
      refresh_token = ''
      
      site_user_auth_info = site_user_auth.objects.filter(user_id=current_user_id, site_id=site_id).first()
      #2 TH đã có trong DB
      if site_user_auth_info:  
        access_token = site_user_auth_info.last_access_token
        refresh_token = site_user_auth_info.last_refresh_token

        print('#2.1 TH đã có trong DB')
        print('#2.1 Get access token : ' + access_token)
        print('#2.1 Get refresh token : ' + refresh_token)

        #2.1 Kiểm tra xem access token còn thời gian không
        is_expires = True
        response_access_token_info = self.call_api_get_access_token_info(access_token)

        if(response_access_token_info.get("expires_in")):
          expires_in = int(response_access_token_info["expires_in"])
          print('#3.1.1 Nếu thời hạn của token nhỏ hơn 10 phút -> Get token mới')
          if expires_in > 6000:
            is_expires = False

        #2.1.1 Nếu thời hạn của token nhỏ hơn 2 phút -> Get token mới
        if is_expires == True:
          response_refresh_access_token = self.call_api_get_refresh_access_token(refresh_token)
          if(response_refresh_access_token.get("access_token")):
            access_token = response_refresh_access_token["access_token"]
          
          if(response_refresh_access_token.get("refresh_token")):
            refresh_token = response_refresh_access_token["refresh_token"]

          #2.3 Update lại refresh token trong DB
          site_user_auth_info = site_user_auth.objects.filter(user_id=current_user_id, site_id=site_id).first()
          site_user_auth_info.last_access_token = access_token
          site_user_auth_info.last_refresh_token = refresh_token
          site_user_auth_info.save()

      # Trả về giá trị access token 
      return access_token
    except Exception as inst:
      #2. Lấy thông tin chi tiết lỗi (Msg, File name, Line number)
      exc_type, ms_tb, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      exc_msg = 'File : {0} | Line : {1} | Type : {2}\nError: {3}'.format(fname, exc_tb.tb_lineno,exc_type,ms_tb)
      
      #3. Lưu vào file erro.log
      logger.error('Exception : ' + str(type(inst)))
      logger.error(exc_msg)

      #4. In ra màn hình console
      print(exc_msg)

  def get_access_token(self, request, site_id):
    try :
      access_token = ''
      refresh_token = ''

      #1. Khởi tạo tên session lưu access token, refresh token theo site
      session_key_access_token = "access_token_" + str(site_id) + "_" + request.user.id
      session_key_refresh_token = "refresh_token_" + str(site_id) + "_" + request.user.id

      #2 Lấy thông tin access token, refresh token
      #2.1 Trường hợp đã có token lưu trong session
      if request.session.get(session_key_access_token) and request.session.get(session_key_refresh_token):
        access_token = request.session.get(session_key_access_token)
        refresh_token = request.session.get(session_key_refresh_token)

      #2.2 Trường hợp chưa lưu access token trong session (Get mới từ access code)
      if access_token == '':
        response_access_token = self.call_api_get_access_token()
        if response_access_token.get("access_token"):
          access_token = response_access_token["access_token"]
          request.session[session_key_access_token] = access_token

        if response_access_token.get("refresh_token"):
          refresh_token = response_access_token["refresh_token"]
          request.session[session_key_refresh_token] = refresh_token
      else :
        #2.3 Trường hợp đã lưu trong session -> Kiểm tra token đã hết hạn
        is_expires = True
        response_access_token_info = self.call_api_get_access_token_info(access_token)

        if(response_access_token_info.get("expires_in")):
          expires_in = int(response_access_token_info["expires_in"])
          #2.3.1 Nếu thời hạn của token nhỏ hơn 2 phút -> Get token mới
          if expires_in > 1200:
            is_expires = False
        
        #2.3.2 Nếu access token đã hết hạn -> Get access token mới từ refresh token
        if is_expires == True:
          response_refresh_access_token = self.call_api_get_refresh_access_token(refresh_token)
          if(response_refresh_access_token.get("access_token")):
            access_token = response_refresh_access_token["access_token"]
            request.session[session_key_access_token] = access_token
          
          if(response_refresh_access_token.get("refresh_token")):
            refresh_token = response_refresh_access_token["refresh_token"]
            request.session[session_key_refresh_token] = refresh_token
            
      # Trả về giá trị access token     
      return access_token
    except Exception as inst:
      #2. Lấy thông tin chi tiết lỗi (Msg, File name, Line number)
      exc_type, ms_tb, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      exc_msg = 'File : {0} | Line : {1} | Type : {2}\nError: {3}'.format(fname, exc_tb.tb_lineno,exc_type,ms_tb)
      
      #3. Lưu vào file erro.log
      logger.error('Exception : ' + str(type(inst)))
      logger.error(exc_msg)

      #4. In ra màn hình console
      print(exc_msg)