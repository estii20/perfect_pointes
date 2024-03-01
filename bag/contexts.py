from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import PointeShoeProduct, Size, Width


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for product_id, item_data in bag.items():
        pointe_shoe_product = get_object_or_404(PointeShoeProduct, pk=product_id)

        if isinstance(item_data, dict):
            for item_key, quantity in item_data.get('items', {}).items():
                size_id, width_id = map(int, item_key.split('_'))

                size = get_object_or_404(Size, pk=size_id)
                width = get_object_or_404(Width, pk=width_id)

                if pointe_shoe_product.price is not None:
                    total += quantity * pointe_shoe_product.price
                    product_count += quantity

                    bag_items.append({
                        'product_id': product_id,
                        'quantity': quantity,
                        'pointe_shoe_product': pointe_shoe_product,
                        'size': size,
                        'width': width,
                    })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
