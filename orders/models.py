from django.db       import models

from products.models import Product, Size
from users.models    import User
from core.models     import TimeStamp

class OrderStatus(models.Model):
  status = models.CharField(max_length=45)

  class Meta:
    db_table = 'order_statuses'

class Order(TimeStamp):
  user            = models.ForeignKey(User, on_delete=models.CASCADE)
  status          = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
  address         = models.CharField(max_length=1000)
  zip_code        = models.CharField(max_length=45)
  recipient       = models.CharField(max_length=45)
  recipient_phone = models.CharField(max_length=45)
  total_price     = models.DecimalField(max_digits=5)

  class Meta:
    db_table = 'orders'

class OrderItemStatus(TimeStamp):
  status = models.CharField(max_length=45)

  class Meta:
    db_table = 'order_item_statuses'

class OrderProduct(TimeStamp):
  order             = models.ForeignKey(Order, on_delete=models.CASCADE)
  product           = models.ForeignKey(Product, on_delete=models.CASCADE)
  size              = models.ForeignKey(Size, on_delete=models.CASCADE)
  order_item_status = models.ForeignKey(OrderItemStatus, on_delete=models.CASCADE)
  count             = models.IntegerField(default=1)

  class Meta:
    db_table = 'order_products'

class Shipment(TimeStamp):
  order           = models.ForeignKey(Order, on_delete=models.CASCADE)
  tracking_number = models.CharField(max_length=200)
  shipment_date   = models.DateField()

  class Meta:
    db_table = 'shipments'

class ShipmentItem(models.Model):
  order    = models.ForeignKey(Order, on_delete=models.CASCADE)
  shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)

  class Meta:
    db_table = 'shipment_items'

