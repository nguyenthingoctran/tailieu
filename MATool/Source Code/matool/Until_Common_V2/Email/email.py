from django.template.loader import render_to_string
from multiprocessing.pool import threading

from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.API.Gmail_API.gmail_api import GmailApi

class Email:
  def draw_email_download_file_layout(self,site_id,download_url,report_type):  
    #1) Get site_info
    if site_id != 0:
      sql_query_site_info = """SELECT * 
                              FROM management_site 
                              WHERE id = {0}""".format(site_id)
      db_controller = db_helper()
      object_site_info = db_controller.query(sql_query_site_info)[0]
    else:
      object_site_info = {'name' : 'All Site'}
    #2) Xuất ra view
    data = {"site_info" : object_site_info,
            "download_url" :download_url,
            'report_type' : report_type}

    layout = render_to_string("email_layout/email_download_file/index.html",data)

    return layout

  # === Hàm để gửi mail ===
  def send_email_download_file(self,site_id,download_url,report_type,list_email,subject,thread_lock):
    #=== Lấy khóa để thực hiện tuần tự ====
    thread_lock.acquire()

    #=== Xử lý gửi email ====
    gmail_api = GmailApi()

    print('===== SEND =====')
    print('=== Đọc file HTML ===')

    html = self.draw_email_download_file_layout(site_id,download_url,report_type)  

    print("=== Email Info ===")

    sender = "noreply@leadplus.app"
    to = ''
    cc = list_email
    subject = subject

    print("=== Sent Email ===")
    message = gmail_api.create_html_message(sender, to, subject, html,cc=cc)

    gmail_api.send_message(sender,message)

    #=== Realead lock ====  
    thread_lock.release()