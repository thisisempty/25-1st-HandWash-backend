import json
from django.core.checks import messages
from django.db.models.aggregates import Count

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from users.models import User
from products.models import Product, ProductSize, Size
from handwash.utils import login_decorator

class CartView(View) :
  @login_decorator
  def post(self, request) :
    data       = json.loads(request.body)

    user       = request.user
    product_id = data['product_id']
    size       = ProductSize.objects.get(name=data['size'])

    try :

      product = Product.objects.get(id=product_id)
      
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
      return JsonResponse({'message' : 'KEY_ERROR'}, status=404)
    
    except Product.DoesNotExist :
      return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=400)
    
  @login_decorator
  def get(self, request) :
    user = request.user
    user_cart = Cart.objects.filter(user_id=user.id).all()

    try :
      results = [{
        'user_id' : user.id,
        'product_list' : [{
          'id' : cart_product.product_id,
          'name' : cart_product.product_set.name,
          'price' : cart_product.product_set.price * cart_product.count,
          'size' : cart_product.size_id,
          'color' : cart_product.color
        }for cart_product in user_cart]
      }]

    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=404)
    
    except Product.DoesNotExist :
      return JsonResponse({'message' : 'PRODUCT_DOES_NOT_EXIST'}, status=400)

    return JsonResponse({'result' : results}, status=200)

  @login_decorator
  def patch(self, request) :
    data = json.loads(request.body)

    user = request.user
    cart_id = data['cart_id']
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
      
      return JsonResponse({'message' : 'SUCCESS', 'total_price' : 30000}, status=200)

    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
  
  @login_decorator
  def delete(self, request) :
    data = json.loads(request.body)

    user = request.user
    product_id = data['product_id']

    if not Cart.objects.filter(user_id=user.id, product_id=product_id).exists() :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    try :
      cart = Cart.objects.filter(user_id=user.id, product_id=product_id)

      if user.id != cart.user_id :
        return JsonResponse({'message' : 'INVAILD_USER'}, status=400)
      
      Cart.objects.filter(id=cart.id).delete()

      return JsonResponse({'message' : 'SUCCESS', 'total_price' : 30000}, status=200)

    
    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'})

    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)








    
    

    

