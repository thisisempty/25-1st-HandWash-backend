from django.urls    import path
from users.views    import LikeView, SignUpView, SignInView

urlpatterns = [
  path('/signup', SignUpView.as_view()),
  path('/signin', SignInView.as_view()),
]