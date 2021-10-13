from django.db       import models

from core.models     import TimeStamp
from products.models import Product
from users.models    import User

class Like(TimeStamp):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  user    = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    db_table = 'likes'