from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Site(models.Model):
  objects         = models.Manager()
  name            = models.CharField(max_length=100)
  url             = models.CharField(max_length=100)
  mode            = models.CharField(max_length=20)
  package         = models.CharField(max_length=20)
  logo            = models.CharField(max_length=255)
  created_date    = models.DateTimeField(auto_now_add=True)
  created_user    = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name + ' - ' + self.url

  class Meta:
    db_table = 'management_site'

class site_user_auth(models.Model):
  objects             = models.Manager()
  site                = models.ForeignKey(Site, on_delete=models.CASCADE)
  user                = models.ForeignKey(User, on_delete=models.CASCADE)
  last_access_token   = models.CharField(max_length=100)
  last_refresh_token  = models.CharField(max_length=100)
  created_date        = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'management_site_user_auth'

class site_auth(models.Model):
  objects                 = models.Manager()
  site                    = models.ForeignKey(Site, on_delete=models.CASCADE)
  last_ga_refresh_token   = models.CharField(max_length=100)
  last_gsc_refresh_token   = models.CharField(max_length=100)
  created_date            = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table = 'management_site_auth'