from django.db       import models
from django.db.models.fields import EmailField

from core.models     import TimeStamp
from products.models import Product, Size

class User(TimeStamp):
  email        = models.CharField(max_length=200, unique=True)
  name         = models.CharField(max_length=45)
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

class Like(TimeStamp):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user    = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    db_table = 'likes'

class Cart(TimeStamp):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user    = models.ForeignKey(User, on_delete=models.CASCADE) 
  size    = models.ForeignKey(Size, on_delete=models.CASCADE)
  count   = models.IntegerField(default=1)

  class Meta:
      db_table = 'carts'
