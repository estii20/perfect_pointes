from django.shortcuts import render
from .models import PointeShoeProduct


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = PointeShoeProduct.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
