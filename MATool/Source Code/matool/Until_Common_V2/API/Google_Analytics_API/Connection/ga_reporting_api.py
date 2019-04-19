import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Analytics_API.google_analytics_API_auth import GAAPIAuth

#Khởi tạo db_helper
db_controller = db_helper()

class GAReportingAPI(GAAPIAuth):
  """
  Class thực hiện truy vấn reporting v4, thực hiện bathGet
  """
  # GOAL
  REST_BATCH_GET_URL     = 'https://analyticsreporting.googleapis.com/v4/reports:batchGet'
  # END GOAL

  def __init__(self,request,site_id):
    GAAPIAuth.__init__(self,request,site_id)

  def test_get_data_by_date(self, start_date, end_date):
    try:
      data = {
              'reportRequests': [
                  {
                      'viewId': self._view_id,
                      # chỉnh ngày tháng năm
                      'dateRanges': [
                          {'startDate': start_date, 'endDate': end_date},
                          #   {'startDate': '2018-10-01', 'endDate': '2018-10-30'},
                      ],
                      # lọc theo cái gì thì chọn ở đây
                      'metrics': [
                          # nếu pageviews mà đi với content group thì lấy được số lần xem trang của group đó
                          {"expression": "ga:pageviews"},
                          {"expression": "ga:uniquePageviews"},
                          {"expression": "ga:timeOnPage"},
                          {"expression": "ga:bounceRate"},
                          {"expression": "ga:exitRate"},
                          {"expression": "ga:sessions"},
                      ],
                      # thứ nguyên chính
                      'dimensions': [
                          {"name": "ga:pagePath"},
                          {"name": "ga:pageTitle"},
                      ],
                  }]
      }

      headers = {
        'authorization': "Bearer " + self._access_token,
        "Content-Type": "application/json"
      }
      result = requests.post(self.REST_BATCH_GET_URL, data=json.dumps(data), headers=headers)
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)

  #HÀM LẤY DỮ LIỆU ALL SITE BÁO CÁO GROUP
  def get_data_for_group_all_by_date(self, start_date, end_date):
    try:
      data = {
              'reportRequests': [
                  {
                      'viewId': self._view_id,
                      #1) chỉnh ngày tháng năm
                      'dateRanges': [
                          {'startDate': start_date, 'endDate': end_date},
                          #1.1)   {'startDate': '2018-10-01', 'endDate': '2018-10-30'},
                      ],
                      #2) lọc theo cái gì thì chọn ở đây
                      'metrics': [
                          #2.1) lấy dữ liệu unique Pageviews
                          {"expression": "ga:uniquePageviews"},
                      ],
                      #3) thứ nguyên chính : lấy theo pagePath và sourceMedium
                      'dimensions': [
                          {"name": "ga:pagePath"},
                          {"name": "ga:sourceMedium"},
                      ],
                      'pageToken' : '',
                      'pageSize' : 1000000
                  }]
      }

      headers = {
        'authorization': "Bearer " + self._access_token,
        "Content-Type": "application/json"
      }
      result = requests.post(self.REST_BATCH_GET_URL, data=json.dumps(data), headers=headers)
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)
  
  #HÀM LẤY DỮ LIỆU CHO GROUP THUỘC SITE KHÁC
  def get_data_for_group_one_by_date(self, start_date, end_date,param_group_id):
    try:
      # 1.1) Get Group Info
      sql_query_group_info = '''SELECT * FROM report_group_setting where id = {0}'''.format(param_group_id)
      object_group_info = db_controller.query(sql_query_group_info)
      #1.2) Url check
      url_check = object_group_info[0]['url_name']
      data = {
              'reportRequests': [
                  {
                      'viewId': self._view_id,
                      #2) chỉnh ngày tháng năm
                      'dateRanges': [
                          {'startDate': start_date, 'endDate': end_date},
                          #2.1)   {'startDate': '2018-10-01', 'endDate': '2018-10-30'},
                      ],
                      #3) lọc theo cái gì thì chọn ở đây
                      'metrics': [
                          #3.1) lấy dữ liệu unique Pageviews                   
                          {"expression": "ga:uniquePageviews"},
                      ],
                      #4) thứ nguyên chính lọc theo pagePathLevel2 và sourceMedium
                      'dimensions': [
                          {"name": "ga:pagePathLevel2"},
                          {"name": "ga:sourceMedium"},

                      ],
                      #5) Lọc thứ nguyên theo chuỗi cần tìm: thêm điều kiện search theo tên group
                      "dimensionFilterClauses": 
                      [
                        {
                          "filters": 
                          [
                            {
                              "dimensionName": "ga:pagePathLevel2",
                              "operator": "REGEXP",
                              "expressions": [url_check]
                            }
                          ]
                        }
                      ],
                      'pageToken' : '',
                      'pageSize' : 1000000
                  }]
      }

      headers = {
        'authorization': "Bearer " + self._access_token,
        "Content-Type": "application/json"
      }
      result = requests.post(self.REST_BATCH_GET_URL, data=json.dumps(data), headers=headers)
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)

  #HÀM LÂY DỮ LIỆU CHO GROUP THUỘC SITE DAC, Vì cách lấy khác Site Sint nên phải viết hàm riêng
  def get_data_for_group_dac_by_date(self, start_date, end_date,param_group_id):
    try:
      # 1.1) Get Group Info
      sql_query_group_info = '''SELECT * FROM report_group_setting where id = {0}'''.format(param_group_id)
      object_group_info = db_controller.query(sql_query_group_info)
      #1.2)check url
      url_check = object_group_info[0]['url_name']
      data = {
              'reportRequests': [
                  {
                      'viewId': self._view_id,
                      #2) chỉnh ngày tháng năm
                      'dateRanges': [
                          {'startDate': start_date, 'endDate': end_date},
                          #2.1)   {'startDate': '2018-10-01', 'endDate': '2018-10-30'},
                      ],
                      #3) lọc theo cái gì thì chọn ở đây
                      'metrics': [
                          #3.1) lấy dữ liệu UniquePage                    
                          {"expression": "ga:uniquePageviews"},
                      ],
                      #4) thứ nguyên chính: Tìm theo pagePathLevel1 và sourceMedium
                      'dimensions': [
                          {"name": "ga:pagePathLevel1"},
                          {"name": "ga:sourceMedium"},
                                    ],
                      #5) Lọc thứ nguyên theo chuỗi cần tìm              
                      "dimensionFilterClauses": 
                      [
                        {
                          "filters": 
                          [
                            {
                              "dimensionName": "ga:pagePathLevel1",
                              "operator": "REGEXP",
                              "expressions": [url_check]
                            }
                          ]
                        }
                      ],           

                      'pageToken' : '',
                      'pageSize' : 1000000
                  }]
      }

      headers = {
        'authorization': "Bearer " + self._access_token,
        "Content-Type": "application/json"
      }
      result = requests.post(self.REST_BATCH_GET_URL, data=json.dumps(data), headers=headers)
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)

  #Hàm lấy dữ liệu cho báo cáo tổng
  def get_data_report_internal(self, start_date, end_date):
    try:
      data = {
              'reportRequests': [
                  {
                      'viewId': self._view_id,
                      #1) chỉnh ngày tháng năm
                      'dateRanges': [
                          {'startDate': start_date, 'endDate': end_date},
                          #1.1)   {'startDate': '2018-10-01', 'endDate': '2018-10-30'},
                      ],
                      #2) lọc theo cái gì thì chọn ở đây
                      'metrics': [
                          #2.1) Lấy dữ liệu sessions, pageviews, bounceRate
                          {"expression": "ga:sessions"},
                          {"expression": "ga:pageviews"},                                   
                          {"expression": "ga:bounceRate"},
                      ],
                      #3) thứ nguyên chính
                      'dimensions': [
                          {"name": "ga:pagePath"},
                          {"name": "ga:sessionDurationBucket"},
                      ],
                      'pageToken' : '',
                      'pageSize' : 1000000
                  }]
      }

      headers = {
        'authorization': "Bearer " + self._access_token,
        "Content-Type": "application/json"
      }
      result = requests.post(self.REST_BATCH_GET_URL, data=json.dumps(data), headers=headers)
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)

  #Hàm lấy số liệu user cho báo cáo tổng
  def get_user_report_internal(self, start_date, end_date):
    try:
      data = {
              'reportRequests': [
                  {
                      'viewId': self._view_id,
                      #1) chỉnh ngày tháng năm
                      'dateRanges': [
                          {'startDate': start_date, 'endDate': end_date},
                          #1.1)   {'startDate': '2018-10-01', 'endDate': '2018-10-30'},
                      ],
                      #2) lọc theo cái gì thì chọn ở đây
                      'metrics': [
                          #2.1) Lấy số liệu users chính xác
                          {"expression": "ga:users"},
                      ],
                      #3) thứ nguyên chính
                      'dimensions': [
                      ],
                      'pageToken' : '',
                      'pageSize' : 1000000
                  }]
      }

      headers = {
        'authorization': "Bearer " + self._access_token,
        "Content-Type": "application/json"
      }
      result = requests.post(self.REST_BATCH_GET_URL, data=json.dumps(data), headers=headers)
      return result.json()    
    except Exception as inst:
      return Log().write_log(inst)
          
