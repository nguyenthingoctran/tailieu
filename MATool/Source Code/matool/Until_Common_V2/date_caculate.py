import time

from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class DateCaculate:
  def get_current_milliseconde(self):
    now = datetime.now()

    millisecond = int(time.mktime(now.timetuple())*1000)
    
    return millisecond
      
  def conver_datetime_to_millisecond(self,date):
    #dayformat 2019-01-31
    list_date = date.split("-")

    t1 = datetime(int(list_date[0]),int(list_date[1]),int(list_date[2]))

    millisecond = int(time.mktime(t1.timetuple())*1000)

    return millisecond

  def conver_millisecond_to_datetime(self,millisecond,format='%Y-%m-%d %H:%M:%S'):  
    date = datetime.fromtimestamp(millisecond/1000.0)

    #dayformat 2019-01-31
    # date = date.strftime('%Y-%m-%d')
    date = date.strftime(format)
    return date

  # lấy ngày đầu tháng tới
  def get_first_date_next_month(self,end_date):
      #day format 2019-01-31 --> 2019-02-01
      change_datetime = datetime.strptime(end_date, "%Y-%m-%d")
      new_date = change_datetime + timedelta(days=1)
      check_time = new_date.strftime('%Y-%m-%d')

      return check_time

  def convert_date_to_month(self,startDate,endDate):
    list_startDate = startDate.split("-")
    list_endDate = endDate.split("-")

    x1 = datetime(int(list_startDate[0]),int(list_startDate[1]),int(list_startDate[2]))
    x2 = datetime(int(list_endDate[0]),int(list_endDate[1]),int(list_endDate[2]))

    list_month = []

    while x2 > x1:
    #thứ 2 là ngày 1, cn là ngày 7   
      day_range = x2.date()

      endDate = x2.strftime("%Y-%m-%d")

      x2 = x2 - timedelta(day_range.day - 1)
      startDate = x2.strftime("%Y-%m-%d")
      x2 = x2 - timedelta(1)

      if(x2 > x1):
        dict_week = {"startDate": startDate, "endDate": endDate}
        list_month.append(dict_week)
      else:
        endDate = (x2 + timedelta(day_range.day)).strftime("%Y-%m-%d")
        startDate = x1.strftime("%Y-%m-%d")
        dict_week = {"startDate": startDate, "endDate": endDate}
        list_month.append(dict_week)
    list_month.reverse()
    return list_month

  #NẾU HÔM NAY KHÔNG PHẢI CUỐI THÁNG THÌ LẤY THÁNG TRƯỚC
  def get_the_most_recent_month(self):
    date = datetime.now()
    date_2 = date + timedelta(days=1)

    if date_2.month > date.month:
      the_most_recent_month = date.strftime('%Y-%m-%d')
    else:
      the_most_recent_month = date - timedelta(days=date.day)
      the_most_recent_month = the_most_recent_month.strftime('%Y-%m-%d')
    return the_most_recent_month

  #Nhập vào start,end xuất ra ['2018年2月','2018年3月','2018年4月']
  def conver_date_to_list_year_month(self,start_date,end_date):
    start_date = start_date.split('-')
    start_date = datetime(int(start_date[0]),int(start_date[1]),int(start_date[2]))

    end_date = end_date.split('-')
    end_date = datetime(int(end_date[0]),int(end_date[1]),int(end_date[2]))

    list_date = []
    while start_date <= end_date:
      # date = str(start_date.year) + '年' + str(start_date.month) +'月'
      date = start_date.strftime("%Y-%m-%d")

      list_date.append(date)

      start_date += relativedelta(months=1)

    return list_date

  #Lấy số tháng mà blog đã đăng
  def get_date_range_by_month(self,date):
    date = date.split('-')
    date = datetime(int(date[0]),int(date[1]),int(date[2]))
    now = datetime.now()

    date_range = now - date
    date_range = date_range.days/30
    date_range = round(date_range,0)
    date_range = int(date_range)
    return date_range
	
  def convert_date_to_week(self,start_date,end_date):
    list_startDate = start_date.split("-")
    list_endDate = end_date.split("-")

    x1 = datetime(int(list_startDate[0]),int(list_startDate[1]),int(list_startDate[2]))
    x2 = datetime(int(list_endDate[0]),int(list_endDate[1]),int(list_endDate[2]))

    list_week = []

    while x2 > x1:
    #thứ 2 là ngày 1, cn là ngày 7 
        day_range = x2.isoweekday()

        endDate = x2.strftime("%Y-%m-%d")

        x2 = x2 - timedelta(day_range - 1)
        startDate = x2.strftime("%Y-%m-%d")
        x2 = x2 - timedelta(1)

        if(x2 > x1):
            dict_week = {"startDate": startDate, "endDate": endDate}
            list_week.append(dict_week)
        else:
            endDate = (x2 + timedelta(day_range)).strftime("%Y-%m-%d")
            startDate = x1.strftime("%Y-%m-%d")
            dict_week = {"startDate": startDate, "endDate": endDate}
            list_week.append(dict_week)
    
    list_week.reverse()
    return list_week

  def convert_date_to_week_2_to_6(self,start_date,end_date):
    list_week = self.convert_date_to_week(start_date,end_date)
    list_week_2_to_6 = []
    for i in list_week:
      end_date = i['endDate'].split("-")
      end_date = datetime(int(end_date[0]),int(end_date[1]),int(end_date[2]))
      end_date = end_date - timedelta(2)
      end_date = end_date.strftime("%Y-%m-%d")
      i['endDate'] = end_date
      list_week_2_to_6.append(i)

    return list_week_2_to_6  