from django.urls import path

from .views import IndexView, ProductListView, basket_add, basket_remove

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='products'),
    # path('page/<int:page>/', ProductListView.as_view, name='paginator'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='products_category'),
    # path('category/<int:cat_id>/page/<int:page>/', products_category, name='paginator_category'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
