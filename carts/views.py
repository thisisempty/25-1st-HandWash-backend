import json
from json.decoder import JSONDecodeError

from django.http      import JsonResponse
from django.views     import View
from django.db.models import F, Sum
from django.db        import transaction

from carts.models    import Cart
from products.models import Product, Size
from handwash.utils  import formatting_price, login_decorator, calculate_delivery_fee

class CartView(View):
  @login_decorator
  def post(self, request):
    data       = json.loads(request.body)

    try:
      product_id = data['product_id']
      size       = Size.objects.get(id=data['size'])

      cart, created = Cart.objects.get_or_create(product_id=product_id, size_id=size.id, user_id=request.user.id)

      if not created :
        cart.count += 1
        cart.save()

      return JsonResponse({'message' : 'SUCCESS'}, status=201)
     
    except KeyError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
    
    except Cart.DoesNotExist:
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    except Size.DoesNotExist:
        return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    except JSONDecodeError:
      return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
    
  @login_decorator
  def get(self, request) :
    cart         = Cart.objects.select_related('product', 'size')\
                               .filter(user_id=request.user.id).order_by('created_at')           
    total_price  = cart.aggregate(total_price=Sum(F('count')*F('product__price')))['total_price']

    try:
      results = {
        'product_list' : [{
          'cart_id'        : cart_product.id,
          'product_id'     : cart_product.product_id,
          'image'          : cart_product.product.mainimage_set.first().url,
          'name'           : cart_product.product.name,
          'price'          : formatting_price(cart_product.product.price),
          'products_price' : formatting_price(cart_product.product.price * cart_product.count),
          'size'           : cart_product.size.size,
          'color'          : cart_product.product.color
        }for cart_product in cart],
        'total_price'  : formatting_price(total_price),
        'delivery_fee' : calculate_delivery_fee(total_price)
      }
      return JsonResponse(results, status=200)

    except KeyError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    except Product.DoesNotExist:
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
    
    except ValueError:
      return JsonResponse({'message' : 'INVALID_VALUE'}, status=400)

  
  @login_decorator
  @transaction.atomic
  def patch(self, request, cart_id):
    data = json.loads(request.body)

    if not Cart.objects.filter(user_id=request.user.id, id=cart_id).exists() :
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)

    try:
      cart = Cart.objects.get(id=cart_id)

      cart.count = data['count']
      cart.save()
      
      return JsonResponse({'message' : 'SUCCESS'}, status=200)

    except KeyError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    except Cart.DoesNotExist:
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)
  
  @login_decorator
  def delete(self, request, cart_id):
    try:
      Cart.objects.get(user_id=request.user.id, id=cart_id).delete()
    
      return JsonResponse({'message' : 'SUCCESS'}, status=200)
    
    except KeyError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    except Cart.DoesNotExist:
      return JsonResponse({'message' : 'DOES_NOT_EXIST'}, status=404)