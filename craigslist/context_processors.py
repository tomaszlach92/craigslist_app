from .models import Category


def static_categories(request):
    """
    :param request:
    Return all categories objects
    """
    return {'static_categories': Category.objects.all(),
            'request': request}
