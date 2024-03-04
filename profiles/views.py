from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from products.models import PointeShoeBrand, Category
from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = Order.objects.filter(user_profile=profile)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'orders': orders, 
        'available_brands': PointeShoeBrand.objects.filter(
            pointeshoe__pointeshoeproduct__availability=True
        ).distinct(),
        'available_categories': Category.objects.filter(
            pointeshoe__pointeshoeproduct__availability=True
        ).distinct(),
        'on_profile_page': True,
        'default_phone_number': profile.default_phone_number,
        'default_country': profile.default_country,
        'default_postcode': profile.default_postcode,
        'default_town_or_city': profile.default_town_or_city,
        'default_street_address1': profile.default_street_address1,
        'default_street_address2': profile.default_street_address2,
        'default_county': profile.default_county,
        'profile': profile, 
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    return render(request, 'checkout/checkout_success.html', {
        'order': order,
        'from_profile': True,
    })