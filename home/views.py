from django.shortcuts import render
from products.models import PointeShoeBrand, Category


def index(request):
    """ A view to return the index page """

    all_brands = PointeShoeBrand.objects.all()
    all_categories = Category.objects.all()

    context = {
        'all_brands': all_brands,
        'all_categories': all_categories,
    }

    return render(request, 'home/index.html', context)
