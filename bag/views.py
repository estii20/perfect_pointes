from django.shortcuts import render, redirect, get_object_or_404
from products.models import PointeShoeBrand, Category, PointeShoeProduct, Size, Width, Color
from bag.contexts import bag_contents


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    """ Add a quantity of the specified product to the shopping bag """

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

    request.session['bag'] = bag
    return redirect(redirect_url)