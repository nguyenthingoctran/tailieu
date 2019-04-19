import pandas as pd
import sys
import os
import logging
import json

from pprint import pprint
from django.http import HttpResponse,StreamingHttpResponse
try:
    from BytesIO import BytesIO 
except ImportError:
    from io import BytesIO 
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

from performance.report_blog_post import get_data_to_report_blog_post
from Until_Common_V2.Microsoft_Office.Excel.draw_excel import DrawExcel
from Until_Common_V2.log import Log

#===========================================================================
#=========== Báo cáo về sessions ===========================================
#===========================================================================
def export_sessions_report_blog_posts_xlsx(file_excel_name,site_id,start_date,end_date):
  try:
    # my "Excel" file, which is an in-memory output file (buffer) 
    # for the new workbook
    output = BytesIO()

    # 1) Lấy dữ liệu từ database
    print("Get data to report")
    list_blog_post_data_table = get_data_to_report_blog_post.get_sessions_blog_post_from_DB(site_id,start_date,end_date)

    # 2)Tạo thư mục chứa file excel
    print("Export excel")
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    #SHEET
    list_blog_excel_sessions_report(writer,list_blog_post_data_table)
    #lưu thành file
    writer.save()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' %file_excel_name

    return response
  except Exception as inst:
    Log().write_log(inst)

def list_blog_excel_sessions_report(writer,list_blog_post_data_table):
  try:
    #1)Những biến cần thiết
    sheet_name = "ブログ一覧_ビュー推移"

    width_table_1 = len(list_blog_post_data_table)

    #2) Vẽ table
    draw_excel = DrawExcel(writer)
    draw_excel.draw_excel_table_only(sheet_name,list_blog_post_data_table)

    # 3) Thêm định dạng 
    # 3.1)Lấy 2 biến này để  thao tác vẽ và format
    workbook  = writer.book
    worksheet = writer.sheets[sheet_name] 

    #3.2)Format
    format1 = workbook.add_format({
        'num_format': '0.00%',
        })

    #3.3)ĐẶT CHIỀU RỘNG CHO CỘT
    worksheet.set_column(0,width_table_1,25)
    #3.4)Tỷ lệ phần trăm
    worksheet.set_column(6,6,None,format1)
  except Exception as inst:
    Log().write_log(inst)

#===========================================================================
#=========== Báo cáo về keyword ============================================
#===========================================================================
def export_keyword_report_blog_posts_xlsx(file_excel_name,site_id,start_date,end_date):
  try:
    # my "Excel" file, which is an in-memory output file (buffer) 
    # for the new workbook
    output = BytesIO()

    # 1) Lấy dữ liệu từ database
    print("Get data to report")
    list_blog_post_data_table = get_data_to_report_blog_post.get_keyword_blog_post_from_DB(site_id,start_date,end_date)

    # 2)Tạo thư mục chứa file excel
    print("Export excel")
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    #SHEET
    list_blog_excel_keyword_report(writer,list_blog_post_data_table)
    #lưu thành file
    writer.save()
    output.seek(0)
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' %file_excel_name

    return response
  except Exception as inst:
    Log().write_log(inst)

def list_blog_excel_keyword_report(writer,list_blog_post_data_table):
  try:
    #1)Những biến cần thiết
    sheet_name = "ブログ一覧_ビュー推移"

    width_table_1 = len(list_blog_post_data_table)

    #2) Vẽ table
    draw_excel = DrawExcel(writer)
    draw_excel.draw_excel_table_only(sheet_name,list_blog_post_data_table)

    # 3) Thêm định dạng 
    # 3.1)Lấy 2 biến này để  thao tác vẽ và format
    workbook  = writer.book
    worksheet = writer.sheets[sheet_name] 

    #3.2)Format
    format1 = workbook.add_format({
        'num_format': '0.00%',
        })

    #3.3)ĐẶT CHIỀU RỘNG CHO CỘT
    worksheet.set_column(0,width_table_1,25)
    #3.4)Tỷ lệ phần trăm
    # worksheet.set_column(6,6,None,format1)
  except Exception as inst:
    Log().write_log(inst)