import jwt

from django.http    import JsonResponse

from handwash.settings import SECRET_KEY
from users.models      import User

def login_decorator(func):
  def wrapper(self, request, *args, **kwargs):
    try:
      access_token = request.headers.get('Authorization')
      payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
      user = User.objects.get(id=payload['id'])
      request.user = user

    except jwt.exceptions.DecodeError:
      return JsonResponse({'MESSAGE' : 'INVALID_TOKEN'}, status = 400)

    except User.DoesNotExist:
      return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

    return func(self, request, *args, **kwargs)

  return wrapper

def formatting_price(price):
    return format(int(price), ',')

def calculate_delivery_fee(total_price):
    return '무료' if total_price >= 30000 or total_price == 0 else '2,500'