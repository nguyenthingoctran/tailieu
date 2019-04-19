import requests
import json

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.API.Google_Analytics_API.Connection.ga_goals_api import GAGoalsAPI

#Khởi tạo db_helper
db_controller = db_helper()

class GAHandleGoalClientAPI(GAGoalsAPI):
  '''Class xử lý Goal Google Analytics API'''
  def __init__(self,request,site_id):
    GAGoalsAPI.__init__(self,request,site_id)

  def get_goal_for_site(self):
    result = self.get_goals()
    return result
