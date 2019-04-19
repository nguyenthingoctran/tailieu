import os
import sys
import requests
import time
import logging
import math
import datetime
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from pprint import pprint

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.log import Log
from Until_Common_V2.enum import LoginStatus, AjaxResponseResult

# Khởi tạo db_helper
db_controller = db_helper()

# =====================================================
# ================== AUTHENTICATION ===================
# =====================================================

# # User (Ajax) : authenticate -> login
def ajax_user_authenticate_login(request):
  if request.method == 'POST':
    if request.is_ajax():
      try:

        result = LoginStatus.invaild.value
        time.sleep(0.3)

        #1. Lấy dữ liệu POST request
        param_user = request.POST['username']
        param_pass = request.POST['password']

        user = authenticate(username=param_user, password=param_pass)
        if user is not None:
          login(request, user)
          result = LoginStatus.success.value
        
      except Exception as inst:
        result = Log().write_log(inst)
        return result

      return HttpResponse(result)
    return HttpResponse()

# User (Ajax) : authenticate -> logout
def ajax_user_authenticate_logout(request):
  if request.method == 'POST':
    if request.is_ajax():
      try:
        result = AjaxResponseResult.success.value
        logout(request)
        
      except Exception as inst:
        result = Log().write_log(inst)
        return result

      return HttpResponse(result)
    return HttpResponse()