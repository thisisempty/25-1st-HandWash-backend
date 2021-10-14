import json
from json.decoder import JSONDecodeError

from django.http      import JsonResponse
from django.views     import View
from django.db.models import F, Sum
from django.db        import transaction

from carts.models    import Cart
from products.models import Product, Size
from handwash.utils  import login_decorator

class CartView(View) :
  @login_decorator
  def post(self, request) :
    data       = json.loads(request.body)

    try :
      product_id = data['product_id']
      size_id    = Size.objects.get(size=data['size']).id

      cart, created = Cart.objects.get_or_create(product_id=product_id, size_id=size_id, user_id=request.user.id)

      if not created :
        cart.count += 1
        cart.save()

      return JsonResponse({'message' : 'SUCCESS'}, status=201)
     
    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
    
    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
 
    except JSONDecodeError :
      return JsonResponse({'message' : "JSON_DECODE_ERROR"}, status=400)
    
  @login_decorator
  def get(self, request) :
    cart    = Cart.objects.filter(user_id=request.user.id).order_by('created_at').all()
    total_price  = cart.aggregate(total_price=Sum(F('count')*F('product__price')))['total_price']

    try :
      results = {
        'product_list' : [{
          'cart_id'        : cart_product.id,
          'product_id'     : cart_product.product_id,
          'image'          : cart_product.product.mainimage_set.first().url,
          'name'           : cart_product.product.name,
          'price'          : format(int(cart_product.product.price),','),
          'products_price' : format(int(cart_product.product.price * cart_product.count), ","),
          'size'           : cart_product.size.size,
          'color'          : cart_product.product.color
        }for cart_product in cart],
        'total_price'  : format(int(total_price), ','),
        'delivery_fee' : '무료' if total_price >= 30000 or total_price == 0 else "2,500"
      }
      return JsonResponse(results, status=200)

    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    except Product.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
    
    except ValueError :
      return JsonResponse({'message' : 'INVALID_VALUE'}, status=400)
  
  @login_decorator
  @transaction.atomic
  def patch(self, request) :
    data       = json.loads(request.body)
    cart_id    = request.GET.get('cart_id')

    if not Cart.objects.filter(user_id=request.user.id, id=cart_id).exists() :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    try :
      cart = Cart.objects.get(id=cart_id)

      cart.count = data['count']
      cart.save()
      
      return JsonResponse({'message' : 'SUCCESS'}, status=200)

    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
  
  @login_decorator
  def delete(self, request) :
    try :
      Cart.objects.get(user_id=request.user.id, id=int(request.GET.get('cart_id'))).delete()
    
      return JsonResponse({'message' : 'SUCCESS'}, status=200)
    
    except KeyError :
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    except Cart.DoesNotExist :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)