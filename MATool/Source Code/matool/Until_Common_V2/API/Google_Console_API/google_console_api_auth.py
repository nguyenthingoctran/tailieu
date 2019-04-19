import os
import sys
import requests
import urllib
import datetime
import logging

from django.http import HttpResponse

from management.models import site_auth
from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log

#Khởi tạo db_helper
db_controller = db_helper()
#Khởi tạo log
log = Log()

# Google Analytics Config (TuanDV)
AUTH_SCOPES = 'https://www.googleapis.com/auth/webmasters.readonly'

AUTH_CLIENT_ID = '357470774416-jb3dkt0k11qjfl6gnnrstdnqngdejh2k.apps.googleusercontent.com'
AUTH_CLIENT_SECRET = 'Yjva2bZXXX9hdIoeOfnvHanH'
AUTH_URL_GET_ACCESS_CODE = 'https://accounts.google.com/o/oauth2/v2/auth'
AUTH_URL_GET_ACCESS_TOKEN = 'https://www.googleapis.com/oauth2/v4/token'

AUTH_STATE_SESSION_NOT_EXISTS = '-1'
AUTH_STATE_EXPRIESED = '0'
AUTH_STATE_AUTHETICATED = '1'


class GSCAPIAuth:

  _client_id = ''
  _client_secret = ''
  _redirect_uri = ''
  _access_code = ''
  _access_token = ''
  _gsc_site_url = ''
  
  def __init__(self,request,site_id, redirect_uri = '', access_code = '') :
    
    sql_query_report_site_info = '''SELECT * FROM management_site_auth WHERE site_id = {0}'''.format(site_id)
    object_report_site_info = db_controller.query(sql_query_report_site_info)
    #lấy giá trị url authen
    param_gsc_site_url = object_report_site_info[0]['gsc_site_url']
    
    self._redirect_uri = redirect_uri
    self._access_code = access_code
    self._client_id = AUTH_CLIENT_ID
    self._client_secret = AUTH_CLIENT_SECRET

    self._access_token = self.get_last_access_token(request, site_id)
    self._gsc_site_url = param_gsc_site_url


  def create_auth_url(self):
    auth_url = AUTH_URL_GET_ACCESS_CODE + '?scope={0}&access_type=offline&prompt=consent&include_granted_scopes=true&redirect_uri={1}&response_type=code&client_id={2}'.format(AUTH_SCOPES, self._redirect_uri, AUTH_CLIENT_ID)
    return auth_url

  def call_api_get_access_token(self):
    try:
      print('--- call_api_get_access_token ---')
      print('code: ' + self._access_code)
      print('client_id: ' + AUTH_CLIENT_ID)
      print('client_secret: '  + AUTH_CLIENT_SECRET)
      print('redirect_uri: '  + self._redirect_uri)
      data = {
          'code' : self._access_code,
          'client_id' : AUTH_CLIENT_ID,
          'client_secret' : AUTH_CLIENT_SECRET,
          'redirect_uri' : self._redirect_uri,
          'grant_type' : 'authorization_code',
          'access_type' : 'offline'
      }

      headers = {"Content-type": "application/json", "Accept": "text/plain"}

      result = requests.post(
          AUTH_URL_GET_ACCESS_TOKEN,
          data,
          headers
      )
      return result.json()
    except Exception as inst:
      return log.write_log(inst)

  def call_api_refresh_access_token(self, refresh_token):
    try:
      data = {
          'client_id' : AUTH_CLIENT_ID,
          'client_secret' : AUTH_CLIENT_SECRET,
          'refresh_token' : refresh_token,
          'grant_type' : 'refresh_token'
      }

      headers = {"Content-type": "application/json", "Accept": "text/plain"}
      
      result = requests.post(
          AUTH_URL_GET_ACCESS_TOKEN,
          data,
          headers
      )
      return result.json()
    except Exception as inst:
      return log.write_log(inst)

  def get_authenticate_state(self, request, site_id):
    try:
      #1. Khởi tạo tên session lưu access token, refresh token theo site
      access_token = ''
      refresh_token = ''
      expires_in = datetime.datetime.now()
      time_now = datetime.datetime.now()
      is_exists_db = False
      is_exists_session = False

      session_key_access_token = "gsc_access_token_" + str(site_id)
      session_key_refresh_token = "gsc_refresh_token_" + str(site_id)
      session_key_expires_in = "gsc_expires_in_" + str(site_id)

      #1.1 Lưu giá trị trạng thái auth mặc định là chưa tồn tại trong session
      authenticate_state = AUTH_STATE_SESSION_NOT_EXISTS
      
      #2 Lấy thông tin access token, refresh token
      #2.1 Trường hợp đã có token lưu trong session
      if request.session.get(session_key_access_token) and request.session.get(session_key_refresh_token) and request.session.get(session_key_expires_in):
        print('#2.1 Trường hợp đã có token lưu trong session')
        access_token = request.session.get(session_key_access_token)
        refresh_token = request.session.get(session_key_refresh_token)
        str_expires_in = request.session.get(session_key_expires_in)
        print(str_expires_in)
        expires_in = datetime.datetime.strptime(str_expires_in, '%Y-%m-%d %H:%M:%S.%f')
        is_exists_session = True

      #2.1 Trường hợp chưa có token lưu trong session
      if not is_exists_session:
        print('#2.1 Trường hợp chưa có token lưu trong session')
        site_auth_info = site_auth.objects.filter(site_id=site_id).first()
        if site_auth_info and site_auth_info.last_gsc_refresh_token != '':
          expires_in = time_now + datetime.timedelta(minutes=50)
          refresh_token = site_auth_info.last_gsc_refresh_token
          is_exists_db = True

      #3 Check expires nếu tồn tại giá trị trong session/db
      if is_exists_db or is_exists_session :
        print('#3 Check expires nếu tồn tại giá trị trong session/db')
        #3.1 Kiểm tra xem access token còn thời gian không
        is_expires = True

        #3.2 Gán trạng thái Auth -> expires
        authenticate_state = AUTH_STATE_EXPRIESED

        if access_token != '':
          print('-- Get Auth info with access code = ' + access_token)
          #3.3 Check is_expries
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
      return authenticate_state
    except Exception as inst:
      return log.write_log(inst)

  def get_last_access_token(self, request, site_id):
    try:
      access_token = ''
      refresh_token = ''
      expires_in = datetime.datetime.now()
      time_now = datetime.datetime.now()
      is_need_refresh_token = False
      is_need_create_token = False

      session_key_access_token = "gsc_access_token_" + str(site_id)
      session_key_refresh_token = "gsc_refresh_token_" + str(site_id)
      session_key_expires_in = "gsc_expires_in_" + str(site_id)
      
      #2 Lấy thông tin access token, refresh token
      #2.1 Trường hợp đã có token lưu trong session
      if request.session.get(session_key_access_token) and request.session.get(session_key_refresh_token):
        print('#2.1 Trường hợp đã có token lưu trong session -> Check expires')
        access_token = request.session.get(session_key_access_token)
        refresh_token = request.session.get(session_key_refresh_token)
        str_expires_in = request.session.get(session_key_expires_in)
        expires_in = datetime.datetime.strptime(str_expires_in, '%Y-%m-%d %H:%M:%S.%f')

        #2.1.1 Trường hợp access token đã hết hạn -> Refresh token
        if time_now >= expires_in:
          is_need_refresh_token = True

      #2.2 Trường hợp chưa có trong session -> Lấy từ DB
      else:
        print('#2.2 Trường hợp chưa có trong session -> Lấy từ DB')
        site_auth_info = site_auth.objects.filter(site_id=site_id).first()
        
        #2.2.1 TH đã có trong DB
        if site_auth_info and site_auth_info.last_gsc_refresh_token != '':
          print('#2.2.1 TH đã có trong DB -> Refresh token')
          is_need_refresh_token = True
        else:
          #2.2.2 TH không có trong DB
          print('#2.2.2 TH không có trong DB')
          is_need_create_token = True

      #3. Cập nhật lại thông tin access token
      if is_need_create_token or is_need_refresh_token :
        #.3.1 Refresh current token
        if is_need_refresh_token :
          #3.1.1 Get site auth info
          site_auth_info = site_auth.objects.filter(site_id=site_id).first()
          refresh_token = site_auth_info.last_gsc_refresh_token

          print('#3.1.2 Refresh new access token from refresh token')
          #3.1.2 Refresh new access token from refresh token
          refresh_access_token_info = self.call_api_refresh_access_token(refresh_token)
          access_token = refresh_access_token_info['access_token']
        #3.2 Create a new token
        else :
          #3.2.1 Create new site auth
          if not site_auth_info:                
            site_auth_info = site_auth()

          print(' #3.2.2 Create new access token')
          #3.2.2 Create new access token
          new_access_token_info = self.call_api_get_access_token()
          print(str(new_access_token_info))
          access_token = new_access_token_info.get('access_token')
          refresh_token = new_access_token_info.get('refresh_token')

        #3.1 Get new session time
        expires_in = time_now + datetime.timedelta(minutes=50)

        print('#3.2 Update/Create DB')
        #3.2 Update/Create DB
        site_auth_info.last_gsc_refresh_token = refresh_token
        #site_auth_info.last_ga_refresh_token = ''
        site_auth_info.site_id = site_id
        site_auth_info.save()
    
        #3.3 Update session
        request.session[session_key_access_token] = access_token
        request.session[session_key_refresh_token] = refresh_token
        request.session[session_key_expires_in] = expires_in.strftime('%Y-%m-%d %H:%M:%S.%f')
      return access_token
    except Exception as inst:
      return log.write_log(inst)
