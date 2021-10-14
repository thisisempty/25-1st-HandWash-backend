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

      like, created = Like.objects.get_or_create(user = user, product_id = data['product_id'])
      
      if not created:
          like.delete()

      return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

    except JSONDecodeError:
      return JsonResponse({'MESSAGE' : 'JSON_DECODE_EEROR'}, status = 400)

  @login_decorator
  def get(self, request):
      user = request.user
      products = Product.objects.filter(like__user_id = user.id)

      try:
        products_user_liked = [{
          'product_id'   : product.id,
          'image'        : product.mainimage_set.first().url,
          'is_conscious' : product.is_conscious,
          'name'         : product.name,
          'price'        : format(int(product.price),','),
          'is_new'       : product.is_new,
          'color'        : product.color,
          'sizes'        : [product.size.size for product in product.productsize_set.all()]
        } for product in products]

        return JsonResponse({
          'MESSAGE' : 'SUCCESS',
          'PRODUCTS_USER_LIKED' : products_user_liked}, 
          status = 201)

      except AttributeError:
        return JsonResponse({"MESSAGE" : 'AttributeError'}, status=400)