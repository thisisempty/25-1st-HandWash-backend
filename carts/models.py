from django.db       import models

from core.models     import TimeStamp
from products.models import Product, Size
from users.models    import User

class Cart(TimeStamp):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user    = models.ForeignKey(User, on_delete=models.CASCADE) 
  size    = models.ForeignKey(Size, on_delete=models.CASCADE)
  count   = models.IntegerField(default=1)

  class Meta:
      db_table = 'carts'