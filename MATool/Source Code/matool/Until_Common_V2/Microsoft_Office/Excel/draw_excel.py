import pandas as pd
from pprint import pprint

class DrawExcel:
  __writer = ''

  def __init__(self,writer):
    self.__writer = writer

  def draw_excel_table_and_avg_table_and_data_table_decreption(self,sheet_name,data_table,pos_row = 0,pos_col = 0,data_table_decreption = {}):
    #===================================================================================
    #================ Tính toàn dữ liệu đầu vào ========================================
    #===================================================================================
    #1) Số hàng, cố cột
    param_row_table = len(list(data_table.values())[0])#6
    param_col_table = len(data_table)#11

    #1.1)Phải đưa hết data_table về dạng list thì mới lọc dược
    list_value_in_data_table = list(data_table.values())

    #1.1.2)dữ liệu 2 ngày gần nhất để tính trung bình
    pre_value = list_value_in_data_table[param_col_table - 2]
    current_value = list_value_in_data_table[param_col_table - 1]

    #1.2)bảng để lưu dữ liệu trung bình
    data_table_avg ={}
    col_avg = []

    for row in range (0,param_row_table):
        try:
            current_value = list_value_in_data_table[param_col_table - 1][row]
            pre_value = list_value_in_data_table[param_col_table - 2][row]
            #1.2.1)Tính trung bình
            if(pre_value == 0 or pre_value == "n/a"):
                value_avg = 0
            else:
                value_avg = round((current_value - pre_value)/pre_value,4)
        #1.2.2)NẾU CHỈ CÓ 1 THÁNG THÌ GÁN THẲNG BẰNG = 0
        except:
            value_avg = round(0,4)
        col_avg.append(value_avg)

    data_table_avg["前月比"] = col_avg
    #===================================================================================
    #=========== Đưa ra file excel =====================================================
    #===================================================================================
    #2) Tạo pandas dataFrame từ date đầu vào
    table = pd.DataFrame(data_table)
    table_avg = pd.DataFrame(data_table_avg)
    table_decription = pd.DataFrame(data_table_decreption)

    #2.1) chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row,index=False)
    table_avg.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col + param_col_table + 1,startrow=pos_row,index = False)
    table_decription.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col + param_col_table + 3,startrow=pos_row,index = False)

    #2.2) Lấy 2 biến này để  thao tác vẽ và format
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 

    #2.2.1) Thêm format
    format1 = workbook.add_format({
        'bold' : True,
        })
    format2 = workbook.add_format({'num_format': '0.00%'})

    # 2.2.2)Đặt kiểu dữ liệu là phần trăm
    worksheet.set_column(param_col_table + 1,param_col_table + 1, None, format2)
    worksheet.set_column(0,0, None, format1)
    
    #2.2.3)Đặt chiều rộng của cột
    worksheet.set_column(0,param_col_table + 4, 11)

  def draw_excel_column_chart_by_row_value(self,sheet_name,data_table,pos_table_row,pos_table_col,pos_chart_row,pos_chart_col):
      # 1) Lấy xlsx self.__writer objects 
      workbook  = self.__writer.book
      worksheet = self.__writer.sheets[sheet_name]

      # 2) Tạo đối tượng chart
      chart = workbook.add_chart({'type': 'column','subtype': 'stacked'})
      chart.set_size({'width': 700, 'height': 250})

      # 3) In dữ liệu chart
      # 3.1)Số hàng, cố cột
      param_row_table = len(list(data_table.values())[0])
      param_col_table = len(data_table)

      # 3.2)Tạo value trong chart
      for row in range(1,param_row_table + 1):   
          chart.add_series({
              # Google/Facebook/Ins
              'name' : [sheet_name, pos_table_row + row, pos_table_col],
              # 2017年8月 / 2017年9月 / 2017年10月
              # [0,0] --- [0,12]
              'categories': [sheet_name, pos_table_row, pos_table_col + 1, pos_table_row, pos_table_col + param_col_table - 1],
              # 10 / 20 / 30
              # [0,0] --- [0,12]
              'values': [sheet_name, pos_table_row + row, pos_table_col + 1, pos_table_row + row, pos_table_col + param_col_table - 1],
          })

      # 4)Thêm chart vào file
      worksheet.insert_chart(pos_chart_row,pos_table_col, chart)

  def draw_excel_column_chart_by_column_value(self,sheet_name,data_table,row_firt_table,row_last_table,pos_table_col,pos_chart_row,pos_chart_col):
      # 1) Lấy xlsx self.__writer objects 
      workbook  = self.__writer.book
      worksheet = self.__writer.sheets[sheet_name]

      # 2) Tạo đối tượng chart
      chart = workbook.add_chart({'type': 'column','subtype': 'stacked'})
      chart.set_size({'width': 700, 'height': 250})

      # 3) In dữ liệu chart

      # 3.1)Tổng Số cột của bảng
      param_col_table = len(data_table)

      # 3.2)Tạo value trong chart Giá trị lấy theo cột
      for col in range(1,param_col_table):   
          chart.add_series({
              # 2017年8月 / 2017年9月 / 2017年10月
              #[0:12]
              'name' : [sheet_name, row_firt_table, col + 1],
              # CEC/ROIT/PBC
              # [0,0] --- [12,0]
              'categories': [sheet_name, row_firt_table + 1, pos_table_col, row_last_table, pos_table_col],
              # 10 / 20 / 30
              # [0,0] --- [0,12]
              'values': [sheet_name, row_firt_table + 1, col + 1, row_last_table, col + 1],
              })
          #Cho label xuống phía dưới
          chart.set_legend({'position': 'bottom'})

      # 3.3) Thêm chart vào file
      worksheet.insert_chart(pos_chart_row,pos_chart_col, chart)   

  #1 table có 3 hàng thì vẽ thành 3 cái chart
  def draw_excel_line_chart_per_table_line(self,sheet_name,data_table,pos_table_row,pos_table_col,pos_chart_row,pos_chart_col):
    # 1) Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    # 2) In dữ liệu chart
    # 2.1)Số hàng, cố cột
    param_row_table = len(list(data_table.values())[0])#2
    param_col_table = len(data_table)#12

    # 2.2)Tạo value trong chart
    # 2.2.1)Độ dài của chart tính bằng col
    chart_col = 0 
    for row in range(1,param_row_table + 1):
      # 2.2.2) Tạo đối tượng chart
      chart = workbook.add_chart({'type': 'line'})
      chart.set_size({'width': 500, 'height': 250})   
      chart.add_series({
          # Google/Facebook/Ins
          'name' : [sheet_name, pos_table_row + row, pos_table_col],
          # 2017年8月 / 2017年9月 / 2017年10月
          # [0,0] --- [0,12]
          'categories': [sheet_name, pos_table_row, pos_table_col + 1, pos_table_row, pos_table_col + param_col_table - 1],
          # 10 / 20 / 30
          # [0,0] --- [0,12]
          'values': [sheet_name, pos_table_row + row, pos_table_col + 1, pos_table_row + row, pos_table_col + param_col_table - 1],
      })

      # 2.2.3)Thêm chart vào file
      worksheet.insert_chart(pos_chart_row,pos_chart_col + chart_col, chart)
      chart_col += 7

  def draw_excel_table_only(self,sheet_name,data_table,pos_row = 0,pos_col = 0,header_bg_color="green",header_font_color="white"):
    #===================================================================================
    #================ Tính toàn dữ liệu đầu vào ========================================
    #===================================================================================
    # 1)Số hàng, cố cột
    param_row_table = len(list(data_table.values())[0])#6
    param_col_table = len(data_table)#11

    #===================================================================================
    #=========== Đưa ra file excel =====================================================
    #===================================================================================
    # 2)Tạo pandas dataFrame từ date đầu vào
    table = pd.DataFrame(data_table)

    # 2.1)chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row + 1,index=False,header=False)

    # 2.2)Lấy 2 biến này để  thao tác vẽ và format
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 

    # 2.3)Thêm format
    format1 = workbook.add_format({
        'align' : 'top',
        'valign' : 'center',
        'text_wrap' : True,
        'bold' : True,
        'border' : 2,
        'bg_color' : header_bg_color,
        'font_color': header_font_color,
        })

    #2.3.1)THÊM FORMAT CHO HEADER
    for col_num, value in enumerate(table.columns.values):
        worksheet.write(pos_row, col_num, value, format1)

  def draw_excel_description_box(self,sheet_name,first_row,first_col,last_row,last_col,header,body):
      # 1) Lấy xlsxself.__writer objects 
      workbook  = self.__writer.book
      worksheet = self.__writer.sheets[sheet_name]

      # 2) Tạo format
      header_format = workbook.add_format({
      'color': '#F79C51',
      'bold' : True,
      'font_size': 20
      })
      body_format = workbook.add_format({
      'font_size': 12
      })
      merge_format = workbook.add_format({
      'bold':     True,
      'border':   6,
      'align':    'top',
      'text_wrap' : True,
      })

      #3) Viết ra file excel
      # 3.1)Merge các cột các hàng lại thành 1 khung lớn
      worksheet.merge_range(first_row,first_col,last_row,last_col,'', merge_format)
      
      # 3.2)Viết ra file excel kèm theo format cho từng chữ
      worksheet.write_rich_string(first_row,first_col,
                                  header_format,header,
                                  body_format,body,merge_format)

  def draw_excel_merge_range(self,sheet_name,first_row,first_col,last_row,last_col,text,bg_color="yellow",font_color='white'):
    # 1) Lấy xlsxself.__writer objects 
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name]

    # 2) Tạo format

    merge_format = workbook.add_format({
    'bold':     True,
    'align':    'center',
    'text_wrap' : True,
    'bg_color': bg_color,
    'font_color': font_color,
    'border' : 1,
    'border_color' : 'white'
    })

    #3) Viết ra file excel
    # 3.1)Merge các cột các hàng lại thành 1 khung lớn
    worksheet.merge_range(first_row,first_col,last_row,last_col,text, merge_format)
  
  def draw_excel_table_not_fomart_header(self,sheet_name,data_table,caption,row_caption,col_caption,pos_row = 0,pos_col = 0,header=True):

    # 1)Số hàng, cố cột
    param_row_table = len(list(data_table.values())[0])#6
    param_col_table = len(data_table)#11

    # 2)Tạo pandas dataFrame từ date đầu vào
    table = pd.DataFrame(data_table)

    # 2.1)chuyển từ dataFrame thành table trong excel
    table.to_excel(self.__writer, sheet_name=sheet_name,startcol = pos_col,startrow=pos_row + 1,index=False,header=header)
    # 2.2)Lấy 2 biến này để  thao tác vẽ và format
    workbook  = self.__writer.book
    worksheet = self.__writer.sheets[sheet_name] 

    #2.2.1) vẽ caption, thêm format
    worksheet.write(row_caption,col_caption,caption,None)
    worksheet.set_column(pos_col-1,pos_col+param_col_table,20)
