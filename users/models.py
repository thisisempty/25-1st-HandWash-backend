from django.db       import models

from core.models     import TimeStamp

class User(TimeStamp):
  email        = models.CharField(max_length=200, unique=True)
  name         = models.CharField(max_length=45, null=True)
  password     = models.CharField(max_length=200)
  birth        = models.DateField()
  last_name    = models.CharField(max_length=45, null=True)
  first_name   = models.CharField(max_length=45, null=True)
  gender       = models.CharField(max_length=45, null=True)
  zip_code     = models.CharField(max_length=20, null=True)
  phone_number = models.CharField(max_length=100, null=True)
  point        = models.IntegerField(default=0)

  class Meta:
    db_table = 'users'



