import json

from django.http          import JsonResponse
from django.views         import View
from json.decoder         import JSONDecodeError

from products.models      import Product
from likes.models         import Like
from handwash.utils       import login_decorator

class LikeView(View):
  @login_decorator
  def post(self, request):
    try:
      data = json.loads(request.body)
      user = request.user

      product_id = data['product_id']

      if not product_id:
        return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

      if not Product.objects.filter(id=product_id).exists():
        return JsonResponse({'MESSAGE' : 'PRODUCT_DOES_NOT_EXIST'}, status = 404)

      product = Product.objects.get(id=product_id)

      if Like.objects.filter(user=user, product=product).exists():
        Like.objects.filter(user=user, product=product).delete()
        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 200)

      Like.objects.create(
        user = user,
        product = product
      )

      return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

    except JSONDecodeError:
      return JsonResponse({'MESSAGE' : 'JSON_DECODE_EEROR'}, status = 400)

  @login_decorator
  def get(self, request):
      user = request.user
      user_likes = Like.objects.filter(user_id=user.id).all()

      try:
        products_user_liked = [{
          'product_id'   : product.product_id,
          'image'        : product.product.mainimage_set.first().url,
          'is_conscious' : product.product.is_conscious,
          'name'         : product.product.name,
          'price'        : format(int(product.product.price),','),
          'is_new'       : product.product.is_new,
          'color'        : product.product.color,
          'sizes'        : [product.size.size for product in product.product.productsize_set.all()]
        } for product in user_likes]

        return JsonResponse({
          'MESSAGE' : 'SUCCESS',
          'PRODUCTS_USER_LIKED' : products_user_liked}, 
          status = 201)

      except AttributeError:
        return JsonResponse({"MESSAGE" : 'AttributeError'}, status=400)