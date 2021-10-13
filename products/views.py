from django.http     import JsonResponse
from django.views    import View

from products.models import *

class CategoryView(View) :
  def get(self, request) :
    category_list = [{
      'id'             : gender_category.id,
      'name'           : gender_category.name,
      'main_category'  : [{
        'id'   : main_category.id,
        'name' : main_category.name,
        'sub_category' : [{
          'id'   : sub_category.id,
          'name' : sub_category.name
        } for sub_category in main_category.subcategory_set.all()]
      } for main_category in gender_category.maincategory_set.all()]
    } for gender_category in GenderCategory.objects.all().order_by('id')]

    return JsonResponse({'category_list':category_list}, status=200)

class ProductListView(View) :
  def get(self, request) :
    limit         = int(request.GET.get('limit', 36))
    offset        = int(request.GET.get('offset', 0))
    order_request = request.GET.get('sort', 'recent')
    
    SORT_PREFIX = {
      'recent'    : '-created_at',
      'old'       : 'created_at',
      'ascPrice'  : 'price',
      'descPrice' : '-price'
    }

    FILTER_PREFIX = {
      'gender'        : 'sub_category__main_category__gender_category__in',
      'main' : 'sub_category__main_category__in',
      'sub'  : 'sub_category__in',
      'color'         : 'color__in',
      'size'          : 'productsize__size__in',
      'collection'    : 'collection__in',
      'conscious'     : 'is_conscious__in',
      'new'           : 'is_new__in'
    }

    filter_set = {
      FILTER_PREFIX.get(key) : value for (key, value) in dict(request.GET).items() if FILTER_PREFIX.get(key)
    }

    try :
      products = Product.objects.filter(**filter_set).order_by(SORT_PREFIX[order_request])

      products_list = [{
        'id'            : product.id,
        'name'          : product.name,
        'price'         : format(int(product.price), ','),
        'is_new'        : product.is_new,
        'is_conscious'  : product.is_conscious,
        'collection_id' : product.collection_id,
        'color'         : [same_product.color for same_product in products.filter(name=product.name, sub_category_id=product.sub_category_id).all()],
        'image'         : [image.url for image in product.mainimage_set.all()]
                      } for product in products[offset:offset+limit]]
    
      return JsonResponse({'products' : products_list}, status=200)
    
    except ValueError:
      return JsonResponse({'message' : 'INVALID_VALUE'}, status=400)


class ProductDetailView(View) :
  def get(self, request, product_id) :
    if Product.objects.get(id=product_id).soft_deleted == 1 :
      return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status=404)
  
    try :
      product = Product.objects.get(id=product_id)

      product_detail = {
        'id'            : product.id,
        'name'          : product.name,
        'price'         : format(int(product.price), ','),
        'main_image'    : [image.url for image in product.mainimage_set.all()],
        'sub_image'     : [image.url for image in product.subimage_set.all()],
        'color'         : [{
          'id'          : color.id,
          'color'       : color.color,
          'image'       : str([image.url for image in color.mainimage_set.all()][0])
                          } for color in Product.objects.filter(name=product.name).all()],
        'size'          : [same_product.size.size for same_product in product.productsize_set.all()],
        'description'   : product.description,
        'length'        : product.length,
        'fit'           : product.fit,
        'configuration' : product.configuration,
        'is_new'        : product.is_new,
        'is_conscious'  : product.is_conscious
      }
      return JsonResponse(product_detail, status=200)
      
    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'})
    
    except Product.DoesNotExist:
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
