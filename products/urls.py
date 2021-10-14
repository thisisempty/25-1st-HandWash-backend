from django.urls import path

from products.views import CategoryView, ProductDetailView, ProductListView

urlpatterns = [
  path('', ProductListView.as_view()),
  path('/categories', CategoryView.as_view()),
  path('/<int:product_id>', ProductDetailView.as_view()),
]