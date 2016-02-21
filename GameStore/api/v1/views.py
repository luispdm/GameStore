__author__ = "Alberto Geniola"
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from Store.models import Game, Category
from api.v1.utils import *
PAGE_SIZE = 10


# Simply print sub-branches for navigation
def v1(request):
    if request.method == "GET":
        return JsonResponse({
            'urls': {
                'self': request.build_absolute_uri(),
                'games': request.build_absolute_uri(reverse('games')),
                'categories': request.build_absolute_uri('categories')
            }
        })
    else:
        # This view only supports GET
        return json_405()


# /api/v1/games/
def games(request):
    """
    List the games of this website. The client may specify some parameters to filter
    the list. Results are ALWAYS paginated in order to save memory and bandwidth.
    It's up to the client to handle pagination navigation.
    Filters:
    -> orderby (optional default is popularity)
    -> name (optional, string to filter game names with)
    -> category (optional, must be an integer representing the category id)
    -> description (optional, string to filter game names with)
    -> page (optional, pagination index. 0 based.)
    :param request:
    :return:
    """
    if request.method == "GET":
        # Filter parameters:
        # orderby, category, name, description
        # page is a mandatory parameter, 0-based

        orderby = request.GET.get('orderby', 'popularity')
        name = request.GET.get('name', None)
        cat = request.GET.get('category', None)
        description = request.GET.get('description', None)
        page = request.GET.get('page', 0)

        # Parameter check
        if orderby not in ['popularity', 'name', 'category', 'price']:
            return json_400("orderby parameter not valid.")
        if cat is not None:
            try:
                cat = int(cat)
            except (ValueError, TypeError):
                return json_400("category parameter not valid. It must be integer.")
        try:
            page = int(page)
        except (ValueError, TypeError):
            return json_400("page parameter not valid. It must be integer.")

        # Prepare the query. This is lazy evaluated.
        l = Game.objects.all()
        if name is not None:
            l = l.filter(name__contains=name)
        if cat is not None:
            l = l.filter(_category__id__exact=cat)
        if description is not None:
            l = l.filter(description__contains=description)

        if orderby == 'category':
            orderby = '_category'

        l = l.order_by(orderby)

        # Pagination math
        pagestart = page*PAGE_SIZE
        pageend = pagestart+PAGE_SIZE
        resnum = l.count()
        pages = int(resnum/PAGE_SIZE)+1

        # This will contain our data
        res = [x.to_json_dict(request.user) for x in l[pagestart:pageend]]

        # Time to send data back to user
        data = {
            'curpage': page,
            'maxpage': pages,
            'games': res
        }

        return JsonResponse(data)
    else:
        # This view only supports GET
        return json_405()


# /api/v1/games/<game-id>
def game(request, game_id):
    """
    Given a game_id, returns details about that specific game.
    :param request:
    :param game_id:
    :return:
    """
    if request.method == "GET":
        try:
            game = Game.objects.get(id=game_id)
        except ObjectDoesNotExist:
            return json_404("Game does not exist.")

        return JsonResponse(data=game.to_json_dict(request.user))

    else:
        # This view only supports GET
        return json_405()


# /api/v1/categories
def categories(request):
    if request.method == "GET":
        cats = [x.to_json_dict() for x in Category.objects.all()]
        res = {}
        res['data'] = cats
        return JsonResponse(res)
    else:
        # This view only supports GET
        return json_405()


# /api/v1/categories/<cat_id>
def category(request, category_id):
    """
    Returns all the games for this category. The same behaviour is obtained
    by searching games directly within the /games branch, however this hierarchy
    is must more rest-friendly.
    :param request:
    :param category_id:
    :return:
    """
    if request.method == "GET":
        try:
            cat = Category.objects.get(id=category_id)
            games = Game.objects.filter(_category__id__exact=category_id)
            resp = cat.to_json_dict()
            resp['games'] = [x.to_json_dict() for x in games]
            return JsonResponse(resp)
        except ObjectDoesNotExist:
            return json_404("Category does not exist.")

    else:
        # This view only supports GET
        return json_405()
