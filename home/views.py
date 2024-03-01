from django.shortcuts import render
from products.models import PointeShoeBrand, Category


def index(request):
    """ A view to return the index page """

    available_brands = (PointeShoeBrand.objects
                        .filter(pointeshoe__pointeshoeproduct__availability=True)
                        .distinct())

    available_categories = (Category.objects
                            .filter(pointeshoe__pointeshoeproduct__availability=True)
                            .distinct())

    context = {
        'available_brands': available_brands,
        'available_categories': available_categories,
    }

    return render(request, 'home/index.html', context)
