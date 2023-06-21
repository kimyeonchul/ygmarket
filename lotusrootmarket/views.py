from django.shortcuts import render
from product.models import Product,ProductSearch
# Create your views here.

def lending(request):
    best_products = Product.objects.order_by('-likes')[:8]
    popular_searches = ProductSearch.objects.all()[:5]
    return render(
        request,
        'lotusrootmarket/lending.html',
        {
            'best_products':best_products,
            'popular_searches': popular_searches,
        }
    )