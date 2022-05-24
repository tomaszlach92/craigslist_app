from .models import Category


def static_categories(request):
    return {'static_categories': Category.objects.all(),
            'request': request}