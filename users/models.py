from django.db       import models

from core.models     import TimeStamp
from products.models import Product, Size

class User(TimeStamp):
  name         = models.CharField(max_length=45)
  password     = models.CharField(max_length=200)
  birth        = models.DateField()
  last_name    = models.CharField(max_length=45)
  first_name   = models.CharField(max_length=45)
  gender       = models.CharField(max_length=45)
  zip_code     = models.CharField(max_length=20)
  phone_number = models.CharField(max_length=100)
  point        = models.IntegerField(default=0)

  class Meta:
    db_table = 'users'

class Like(TimeStamp):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    db_table = 'likes'

class Cart(TimeStamp):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE) 
  size = models.ForeignKey(Size, on_delete=models.CASCADE)
  count = models.IntegerField(default=1)

  class Meta:
      db_table = 'carts'
