"""
Database controller
"""
from django.db import connection
import logging
import sys
import os

from Until_Common_V2.log import Log

class db_helper:

  _db_name = ''

  def __init__(self):
    _db_name = ''

  def _dictfetchall(self, cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

  def _dictfetchone(self, cursor):
    "Return one row from a cursor as a dict"
    columns = (col[0] for col in cursor.description)
    result = cursor.fetchone()
    result = dict(zip(columns, result))
    return result

  def query_scalar_bak(self, sql):
    try:
      with connection.cursor() as cursor:
        cursor.execute(sql)
        return self._dictfetchone(cursor)
    except Exception as inst:
      Log().write_log(inst)

  def query_scalar(self, sql):
    try:
      object_info = self.query(sql)
      if len(object_info) > 0:
        return object_info[0]
      else:
        return False
    except Exception as inst:
      Log().write_log(inst)
    
  def query(self, sql):
    try:
      with connection.cursor() as cursor:
        cursor.execute(sql)
        return self._dictfetchall(cursor)
    except Exception as inst:
      Log().write_log(inst)

  def execute(self, sql):
    try:
      cursor = connection.cursor()
      cursor.execute(sql)
      rows_updated = cursor.rowcount
      connection.commit()
      connection.close()

      # Trả về số bản ghi được update
      return rows_updated
    except Exception as inst:
      Log().write_log(inst)
