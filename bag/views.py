from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages

from products.models import PointeShoeBrand, Category, PointeShoeProduct, Size, Width, Color
from bag.contexts import bag_contents


def view_bag(request):
    """ A view that renders the bag contents page """

    available_brands = PointeShoeBrand.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()
    available_categories = Category.objects.filter(pointeshoe__pointeshoeproduct__availability=True).distinct()

    context = {
        'available_brands': available_brands,
        'available_categories': available_categories,
    }

    return render(request, 'bag/bag.html', context)


def add_to_bag(request, product_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(PointeShoeProduct, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    size_id = request.POST.get('size_id')
    width_id = request.POST.get('width_id')
    redirect_url = request.POST.get('redirect_url')

    item_key = f"{size_id}_{width_id}"

    bag = request.session.get('bag', {})

    if product_id in bag:
        if item_key in bag[product_id]['items']:
            bag[product_id]['items'][item_key] += quantity
        else:
            bag[product_id]['items'][item_key] = quantity
    else:
        bag[product_id] = {'items': {item_key: quantity}}
        messages.success(request, f'Added {product.title} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, product_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(PointeShoeProduct, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    size_id = request.POST.get('size_id')
    width_id = request.POST.get('width_id')

    item_key = f"{size_id}_{width_id}"

    bag = request.session.get('bag', {})

    if product_id in bag and item_key in bag[product_id]['items']:
        if quantity > 0:
            bag[product_id]['items'][item_key] = quantity
            messages.success(request, f'Updated {product.title} quantity to {quantity}')
        else:
            del bag[product_id]['items'][item_key]
            if not bag[product_id]['items']:
                bag.pop(product_id)
            messages.success(request, f'Removed {product.title} from your bag')

        request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, product_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(PointeShoeProduct, pk=product_id)
        size_id = request.POST.get('size_id')
        width_id = request.POST.get('width_id')
        item_key = f"{size_id}_{width_id}"
        
        bag = request.session.get('bag', {})
        del bag[product_id]['items'][item_key]
        if not bag[product_id]['items']:
            bag.pop(product_id)
        messages.success(request, f'Removed {product.title} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
