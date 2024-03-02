import json
import stripe
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from bag.contexts import bag_contents
from products.models import (
    PointeShoeProduct, PointeShoeBrand, Category
)
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from .forms import OrderForm
from .models import Order, OrderLineItem


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                'bag': json.dumps(request.session.get('bag', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            }
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.'
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)

            order.save()

            user = request.user
            profile_data = {
                'default_phone_number': form_data['phone_number'],
                'default_country': form_data['country'],
                'default_postcode': form_data['postcode'],
                'default_town_or_city': form_data['town_or_city'],
                'default_street_address1': form_data['street_address1'],
                'default_street_address2': form_data['street_address2'],
                'default_county': form_data['county'],
                'user_id': user.id  
            }

            profile, created = UserProfile.objects.get_or_create(user=user, defaults=profile_data)

            for product_id, item_data in bag.items():
                product = get_object_or_404(PointeShoeProduct, pk=product_id)
                if isinstance(item_data, int):
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                else:
                    for size_width, quantity in item_data['items'].items():
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                        order_line_item.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('view_bag'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

        available_brands = PointeShoeBrand.objects.filter(
            pointeshoe__pointeshoeproduct__availability=True).distinct()
        available_categories = Category.objects.filter(
            pointeshoe__pointeshoeproduct__availability=True).distinct()

        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'available_brands': available_brands,
            'available_categories': available_categories,
        }

        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    bag = request.session.get('bag', {})
    line_items = order.lineitems.all()

    for item in line_items:
        selected_size = item.product.pointe_shoe.available_sizes.first()
        selected_width = item.product.pointe_shoe.available_widths.first()

        if selected_size:
            item.product_size = str(selected_size.size)
        if selected_width:
            item.product_width = str(selected_width.width)

        product_title = item.product.title
        product_color_friendly_name = item.product.pointe_shoe.color.get_friendly_name()

        item.product_title = product_title
        item.product_color = product_color_friendly_name
        item.save()

    if 'bag' in request.session:
        del request.session['bag']

    available_brands = (
        PointeShoeBrand.objects
        .filter(pointeshoe__pointeshoeproduct__availability=True)
        .distinct()
    )
    available_categories = (
        Category.objects
        .filter(pointeshoe__pointeshoeproduct__availability=True)
        .distinct()
    )

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'line_items': line_items,
        'available_brands': available_brands,
        'available_categories': available_categories,
    }

    return render(request, template, context)


def repurchase_product(request, product_id):
    """
    After checkout repurchase product
    """
    product = get_object_or_404(PointeShoeProduct, pk=product_id)

    messages.success(request, f"Redirecting to {product.title} for repurchase.")

    return redirect(reverse('product_detail', args=[product_id]))
