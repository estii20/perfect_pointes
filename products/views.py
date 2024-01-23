from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import PointeShoeProduct, PointeShoe, Category, PointeShoeBrand, Color


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = PointeShoeProduct.objects.all()
    query = None
    categories = None
    brands = None
    colors = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET.getlist('category')
            products = products.filter(pointe_shoe__category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'brand' in request.GET:
            brands = request.GET.getlist('brand')
            products = products.filter(brand__name__in=brands)
            brands = PointeShoeBrand.objects.filter(name__in=brands)

        if 'color' in request.GET:
            colors = request.GET.getlist('color')
            color_objects = Color.objects.filter(name__in=colors)
            products = products.filter(pointe_shoe__color__in=color_objects)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(title__icontains=query) | Q(pointe_shoe__description__icontains=query)
            products = products.filter(queries)

    all_categories = Category.objects.all()
    all_brands = PointeShoeBrand.objects.all()
    all_colors = Color.objects.all()

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'all_categories': all_categories,
        'current_brands': brands,
        'all_brands': all_brands,
        'current_colors': colors,
        'all_colors': all_colors,
        'current_sorting': current_sorting,
    }

    if query:
        context['search_term'] = query

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(PointeShoeProduct, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
