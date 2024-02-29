from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import PointeShoeProduct, PointeShoe, Category, PointeShoeBrand, Color
from .forms import PointeShoeProductForm, PointeShoeProductEditForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = PointeShoeProduct.objects.filter(availability=True)
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
                products = products.annotate(lower_name=Lower('title'))
            elif sortkey == 'color':
                sortkey = 'pointe_shoe__color__name'
                products = products.order_by(sortkey)

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

            queries = Q(title__icontains=query) | Q(pointe_shoe__feature__icontains=query)
            products = products.filter(queries)

    all_categories = Category.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()
    all_brands = PointeShoeBrand.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()
    all_colors = Color.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()

    available_brands = all_brands.filter(id__in=products.values_list('brand__id', flat=True))
    available_categories = all_categories.filter(id__in=products.values_list('pointe_shoe__category__id', flat=True))
    available_colors = all_colors.filter(id__in=products.values_list('pointe_shoe__color__id', flat=True))

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
        'available_brands': available_brands,
        'available_categories': available_categories,
        'available_colors': available_colors,
    }

    if query:
        context['search_term'] = query

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    available_brands = PointeShoeBrand.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()
    available_categories = Category.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()
    available_colors = Color.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()
    product = get_object_or_404(PointeShoeProduct, pk=product_id)

    context = {
        'available_brands': available_brands,
        'available_categories': available_categories,
        'available_colors': available_colors,
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = PointeShoeProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = PointeShoeProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(PointeShoeProduct, pk=product_id)
    if request.method == 'POST':
        form = PointeShoeProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = PointeShoeProductEditForm(instance=product)
        messages.info(request, f'You are editing {product.title}')

    available_brands = PointeShoeBrand.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()
    available_categories = Category.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
        'available_brands': available_brands,
        'available_categories': available_categories,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(PointeShoeProduct, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
