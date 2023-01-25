from django.http import HttpResponseRedirect

from .models import ProductCategory, Product, Basket
from django.contrib.auth.decorators import login_required
from common.views import TitleMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView



class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = "Store"


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    context_object_name = 'products'
    title = 'Store - Products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['category'] = ProductCategory.objects.filter(product__isnull=False).distinct()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

# def index(request):
#     context = {
#         'title': 'Store',
#         'is_prom': False,
#     }
#     return render(request, 'products/index.html', context=context)


# def products(request, page=1):
#     product = Product.objects.filter(quantity__gt=0)
#     per_page = 3
#     paginator = Paginator(product, per_page)
#     product_paginator = paginator.page(page)
#
#     context = {
#         'title': 'Store - Products',
#         'products': product_paginator,
#         'category': ProductCategory.objects.filter(product__isnull=False).distinct(),
#     }
#     return render(request, 'products/products.html',  context=context)


# def products_category(request, cat_id, page=1):
#     product = Product.objects.filter(category=cat_id)
#     per_page = 3
#     paginator = Paginator(product, per_page)
#     product_paginator = paginator.page(page)
#     context = {
#         'title': f'Store - {ProductCategory.objects.get(pk=cat_id)}',
#         #'products': Product.objects.filter(category=cat_id).order_by('-price'),
#         'products': product_paginator,
#         'category': ProductCategory.objects.filter(product__isnull=False).distinct(),
#     }
#     return render(request, 'products/products.html',  context=context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.last()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(pk=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
