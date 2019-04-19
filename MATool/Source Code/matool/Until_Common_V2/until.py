import io

from pdf2image import convert_from_path,convert_from_bytes
from datetime import datetime

from Until_Common_V2.log import Log

def conver_pdf_to_image_bytes(my_file):
  try:
    # creating an object 
    print("%50s"%"CONVER PDF TO IMAGE")

    pages = convert_from_bytes(my_file, 50)
    # pages[0].save('Page_0.jpg', 'JPEG')

    print("%50s"%"IMAGE TO BYTES")

    byteImgIO = io.BytesIO()
    pages[0].save(byteImgIO, "PNG")
    byteImgIO.seek(0)
    byteImg = byteImgIO.read()
    
    return byteImg
  except Exception as e:
    result = Log().write_log(e)
    return result

def get_day_subject_in_email():
  week_days = ("（月）","（火）","（水）","（木）","（金）","（土）","（日）")
  time_now = datetime.now()
  time_now_week_day = time_now.weekday()
  time_now_format = '{0}年{1}月{2}日{3}'.format(time_now.year, time_now.month, time_now.day,week_days[time_now_week_day]) 

  return time_now_format

def sql_query_cover_special_charater(input_string):
  input_string = input_string.replace("'","\\'")
  input_string = input_string.replace('"','\\"')

  return input_string