import os
import sys
import logging

from enum import Enum

class AjaxResponseResult(Enum):
  success = 1
  error   = 0

class Log:
  def write_log(self,inst):
    logger = logging.getLogger(__name__)
    #1. Trường hợp là hàm Ajax thì trả về giá trị AjaxResponseResult = -1
    result = AjaxResponseResult.error.value

    #2. Lấy thông tin chi tiết lỗi (Msg, File name, Line number)
    exc_type, ms_tb, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    exc_msg = 'File : {0} | Line : {1} | Type : {2}\nError: {3}'.format(fname, exc_tb.tb_lineno,exc_type,ms_tb)
    
    #3. Lưu vào file erro.log
    print("%50s"%"====== ERROR ======")
    logger.error('Exception : ' + str(type(inst)))
    logger.error(exc_msg)
    print("%53s"%"====== END ERROR ======")
    #4. In ra màn hình console
    # print(exc_msg)

    return result