from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import PointeShoeProduct, PointeShoe


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = PointeShoeProduct.objects.all()
    query = None

    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('products'))

        queries = Q(title__icontains=query) | Q(pointe_shoe__feature__icontains=query) | Q(brand__name__icontains=query)
        products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(PointeShoeProduct, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
