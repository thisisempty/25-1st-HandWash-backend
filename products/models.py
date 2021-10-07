from django.db   import models
from django.db.models.deletion import CASCADE

from core.models import TimeStamp

class GenderCategory(TimeStamp):
  name = models.CharField(max_length=45)

  class Meta:
    db_table = 'gender_categories'

class MainCategory(TimeStamp):
  gender_category = models.ForeignKey(GenderCategory, on_delete=models.CASCADE)
  name            = models.CharField(max_length=45)

  class Meta:
    db_table = 'main_categories'

class SubCategory(TimeStamp):
  main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
  name          = models.CharField(max_length=45)

  class Meta:
    db_table = 'sub_categories'

class Collection(models.Model):
  name = models.CharField(max_length=45)

  class Meta:
    db_table = 'collections'

class Product(TimeStamp):
  sub_category  = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
  collection     = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)
  name          = models.CharField(max_length=45)
  price         = models.DecimalField(max_digits=10, decimal_places=5)
  color         = models.CharField(max_length=45)
  description   = models.CharField(max_length=1000)
  length        = models.CharField(max_length=45)
  fit           = models.CharField(max_length=45)
  configuration = models.CharField(max_length=100)
  is_new        = models.BooleanField(default=1)
  is_conscious  = models.BooleanField(default=0)
  soft_deleted  = models.BooleanField(default=0)

  class Meta:
    db_table = 'products'

class Size(models.Model):
  size = models.CharField(max_length=45)

  class Meta:
    db_table = 'sizes'

class ProductSize(models.Model):
  product = models.ForeignKey(Product, on_delete=CASCADE)
  size    = models.ForeignKey(Size, on_delete=CASCADE)

  class Meta:
    db_table = 'products_sizes'

class Image(models.Model):
  url     = models.CharField(max_length=500)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)

  class Meta:
    db_table = 'images'

class Material(models.Model):
  name = models.CharField(max_length=45)

  class Meta:
    db_table = 'materials'

class ProductMaterial(models.Model):
  product  = models.ForeignKey(Product, on_delete=CASCADE)
  material = models.ForeignKey(Material, on_delete=CASCADE)

  class Meta:
    db_table = 'products_materials'
