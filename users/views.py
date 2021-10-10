import json, re, bcrypt, jwt

from django.http            import JsonResponse
from django.views           import View

from users.models           import User
from handwash.my_settings   import SECRET_KEY, ALGORITHM
from handwash.utils         import login_decorator

class SignUpView(View):
  def post(self, request):
    data = json.loads(request.body)

    email    = data['email']
    password = data['password']
    birth    = data['birth']

    EMAIL_REGEX    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

    try:
      if not re.match(EMAIL_REGEX, email):
        return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status=400)

      if not re.match(PASSWORD_REGEX, password):
        return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status=400)

      if User.objects.filter(email = email).exists():
        return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXISTS'}, status=400)

      hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      decoded_pw = hashed_pw.decode('utf-8')

      User.objects.create(
        email        = email,
        password     = decoded_pw,
        birth        = birth,
        name         = data.get('name'),
        last_name    = data.get('last_name'),
        first_name   = data.get('first_name'),
        gender       = data.get('gender'),
        zip_code     = data.get('zip_code'),
        phone_number = data.get('phone_number'),
        point        = data.get('point', 0),
      ) 

      return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

    except KeyError:
      return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

class SignInView(View):
  def post(self, request):
    try :
      data = json.loads(request.body)

      email    = data['email']
      password = data['password']

      if not User.objects.filter(email = email).exists():
        return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 401)

      user = User.objects.get(email = email)
      if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 401)

      access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
      return JsonResponse({'ACCESS_TOKEN' : access_token}, status = 200)

    except KeyError :
      return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)