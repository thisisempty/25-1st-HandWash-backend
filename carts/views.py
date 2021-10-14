import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.models import F, Sum

from carts.models import Cart
from products.models import Product, ProductSize, Size
from handwash.utils import login_decorator

class CartView(View) :
  @login_decorator
  def post(self, request) :
    data       = json.loads(request.body)

    user       = request.user
    product_id = data['product_id']

    try :
      size       = Size.objects.get(size=data['size']).id
      product    = Product.objects.get(id=product_id)
      
      if not ProductSize.objects.get(product_id=product_id, size_id=size) :
        return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

      if Cart.objects.filter(user_id=user.id, product_id=product.id, size_id=size).exists() :
        cart = Cart.objects.get(product_id=product.id, size_id=size)

        cart.count += 1
        cart.save()
      
      else :
        Cart.objects.create(
        user_id    = user.id,
        product_id = product.id,
        size_id    = size
      )

      return JsonResponse({'message' : 'SUCCESS'}, status=201)
     
    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
    
    except Product.DoesNotExist :
      return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)
    
    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    except ProductSize.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status=404)
    
    except Size.DoesNotExist :
      return JsonResponse({'message' : "DOES_NOTE_EXIST"}, status=404)

    except JSONDecodeError :
      return JsonResponse({'message' : "JSON_DECODE_ERROR"}, status=400)
    
  @login_decorator
  def get(self, request) :
    user        = request.user
    user_cart   = Cart.objects.filter(user_id=user.id).all()
    total_price = user_cart.aggregate(total_price=Sum(F('count')*F('product__price')))['total_price']

    try :
      results = {
        'product_list' : [{
          'cart_id' : cart_product.id,
          'product_id'      : cart_product.product_id,
          'image'   : cart_product.product.mainimage_set.first().url,
          'name'    : cart_product.product.name,
          'price'   : format(int(cart_product.product.price),','),
          'products_price'   : format(int(cart_product.product.price * cart_product.count), ","),
          'size'    : cart_product.size.size,
          'color'   : cart_product.product.color
        }for cart_product in user_cart],
        'total_price' : format(int(total_price), ',')
      }
      return JsonResponse(results, status=200)

    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    except Product.DoesNotExist :
      return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)
    
    except ValueError :
      return JsonResponse({'message' : 'INVALID_VALUE'}, status=400)
    
  @login_decorator
  def patch(self, request) :
    data = json.loads(request.body)

    user       = request.user
    cart_id    = data['cart_id']
    product_id = data['product_id']

    if not Cart.objects.filter(user_id=user.id, product_id=product_id).exists() :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    try :
      cart = Cart.objects.get(id=cart_id)

      if user.id != cart.user_id :
        return JsonResponse({'message' : 'INVAILD_USER'}, status=400)

      if not cart.product_id != product_id :
        return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=404)

      cart.count = data['count']
      cart.save()
      
      return JsonResponse({'message' : 'SUCCESS'}, status=200)

    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
  
  @login_decorator
  def delete(self, request) :
    data = json.loads(request.body)

    user       = request.user
    product_id = data['product_id']
    size       = Size.objects.get(size=data['size']).id

    if not Cart.objects.filter(user_id=user.id, product_id=product_id, size_id=size).exists() :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    try :
      cart = Cart.objects.get(user_id=user.id, product_id=product_id, size_id=size)
      
      Cart.objects.filter(id=cart.id).delete()
    
      return JsonResponse({'message' : 'SUCCESS'}, status=200)
    
    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)








    
    

    

