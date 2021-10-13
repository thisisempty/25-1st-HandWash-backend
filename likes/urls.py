from django.urls    import path

from likes.views    import LikeView

urlpatterns = [
  path('/like', LikeView.as_view()),
]