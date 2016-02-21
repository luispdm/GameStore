from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, permission_required
from .forms import GameForm, CartForm
from .models import Game, Order
from hashlib import md5
from django.http import HttpResponse
from django.db.models import Count
import json
import datetime
from django.contrib.auth.decorators import user_passes_test
from common.utils import user_is_developer, user_is_player



# ---------------------- PUBLIC VIEWs ---------------------- #

# Public view: no authentication required.
def home(request):
    return render(request=request, template_name='store/home.html')


# Public view, no authentication required
def list_games(request):
    return render(request=request, template_name='store/list_games.html')


# ---------------------- PLAYERS' VIEWs ---------------------- #

@login_required(login_url='login')
@user_passes_test(user_is_player, login_url='login')
def my_games(request):
    games = [x.to_json_dict(request.user) for x in request.user.profile._ownedGames.all()]
    # Return a list of games owned by the logged user
    return render(request, 'store/my_games.html', {'user': request.user, 'games': games})


@login_required(login_url='login')
# @user_passes_test(user_is_player, login_url='login') # This view can serve back Ajax. In this case
# we want to populate error field in this case.
def cart(request):
    """
    This view handles the shopping cart.
    GET-> Show the cart status
    POST-> Handle a request, that might be add a game to the cart or remove a game from the cart.
    DEL/PUT not supported.

    POST Parameters:
        action: <"add" | "remove">
        game_id: <integer>
        next: <url for optional redirection>

    Only accessible through ajax

    :param request:
    :return:
    """
    if not request.user.profile.is_player:
        messages.warning(request, "Only player profiles can buy from the shop. Log-in/register as a player first.")
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'GET':
        # When requesting this page with GET, we simply return the cart status.
        # The cart status is mapped in the session variable cart_items, which is an array
        # that contains a list of IDs of games. Every time this page is requested,
        # the games data is update
        game_ids = request.session.get('cart_items', [])
        return render(request, 'store/cart.html', {'user': request.user, 'cart':  to_client_cart(game_ids)})

    elif request.method == 'POST':
        if not request.is_ajax():
            messages.error(request, "This view can be only accessed through ajax calls.")
            return HttpResponseRedirect(reverse("cart"))

        jsondata = {'error': None}

        if not user_is_player(request.user):
            jsondata['error'] = "You are not a player, thus you can not purchase any game."
            return JsonResponse(status=403, data=jsondata)

        # Validate the form with the basic validation provided by the form object
        form = CartForm(request.POST)
        if not form.is_valid():
            jsondata['error'] = form.errors
            return JsonResponse(status=400, data=jsondata)

        # More complex validation, dependent on the user's session & user state
        if form.cleaned_data['action'] == 'add':

            # The user should not have the game already
            owned_games = request.user.profile._ownedGames.filter(id__exact=form.cleaned_data['game'].id)
            if owned_games.count() > 0:
                jsondata['error'] = "You already own this game"

            curcart = request.session.get('cart_items',[])
            # The cart-session should not contain the same game
            if form.cleaned_data['game'].id in curcart:
                jsondata['error'] = "The cart already contains this game"

            if jsondata['error'] is None:
                # Ok, add the game into the session vars
                curcart.append(form.cleaned_data['game'].id)
                request.session['cart_items'] = curcart

        elif form.cleaned_data['action'] == 'remove':
            # The session should contain the same game
            items = request.session.get('cart_items', [])
            if form.cleaned_data['game'].id in items:
                items.remove(form.cleaned_data['game'].id)
                request.session['cart_items'] = items

        else:
            jsondata['error'] = "Invalid action requested."

        if jsondata['error'] is not None:
            return JsonResponse(status=400, data=jsondata)
        else:
            return JsonResponse(status=201, data=jsondata)

    else:
        # This view only supports GET & POST
        return HttpResponse(status=405, content="Invalid method.")


#TODO transaction!
@login_required(login_url='login')
@user_passes_test(user_is_player, login_url='login')
def orders(request):
    if request.method == 'GET':
        # List all the orders performed by this user
        orders = Order.objects.filter(_player=request.user.profile)

        return render(request, 'store/orderlist.html', {'user': request.user,
                                                        'orders': orders})

    elif request.method == 'POST':
        # Create a new order
        game_ids = request.session.get('cart_items', [])
        total = 0.0
        qset = Game.objects.filter(id__in=game_ids)

        # Check if the user already owns any of those games. If so, just notify him with a message and remove it from
        # the list. Contextually, calculate the total
        for g in qset:
            if request.user.profile._ownedGames.filter(id__exact=g.id).count() > 0:
                messages.error(request,"You already own the game %s. This item has been removed from the cart"
                                 % g.name)
                game_ids.remove(g.id)
            else:
                total += g.price

        # Delete any previous pending orders associated with the user
        Order.objects.filter(_player=request.user.profile, status="pending").delete()

        # Get all valid games, game_ids has been purged
        qset = Game.objects.filter(id__in=game_ids)

        # If somehow the cart is empty, deny the order creation and redirect the user to the cart.
        if qset.count() < 1:
            messages.warning(request, "The cart is empty!")
            return HttpResponseRedirect(reverse("cart"))

        # Create a Order to temporary store the order intention by the user
        order = Order.objects.create(_player=request.user.profile,
                                     total=total,
                                     orderDate=datetime.datetime.now(),
                                     paymentDate=None,
                                     paymentRef=None,
                                     status="pending")
        order._games = qset.all()
        order.save()

        messages.info(request, "Order created successfully.")

        # Retrieve the ID and redirect the user to the order detailed view.
        return HttpResponseRedirect(reverse("order_details", kwargs={'order_id':order.id}))

    else:
        # This view only supports GET & POST
        return HttpResponse(status=405, content="Invalid method.")


#TODO transaction!
@login_required(login_url='login')
@user_passes_test(user_is_player, login_url='login')
def order_details(request, order_id):
    if request.method == 'GET':
        # Print order status
        # Do we have the pid?
        if order_id is None:
            messages.error(request, "Invalid or missing Pid specified.")
            return HttpResponseRedirect(reverse("cart"))

        pid = order_id

        # Does it correspond to a real one?
        order = None
        try:
            order = Order.objects.get(id=pid)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid or missing Pid specified.")
            return HttpResponseRedirect(reverse("cart"))

        # Is the user in charge of it?
        if order._player != request.user.profile:
            messages.error(request, "You are not allowed to manage this order")
            return HttpResponseRedirect(reverse("cart"))

        # Is the associated pid in a correct status?
        if order.status != "pending" and order.status != "error":
            messages.error(request, "The specified order is not on a valid status to be processed again.")
            return HttpResponseRedirect(reverse("cart"))

        # Ok, everything seems fine. Print again the submit form.
        action = "http://payments.webcourse.niksula.hut.fi/pay/"  # Fixme Todo: parametrize
        amount = order.total
        sid = "italiancrea2016"  # Fixme Todo: parametrize
        success_url = request.build_absolute_uri(reverse("payment_result"))
        cancel_url = request.build_absolute_uri(reverse("payment_result"))
        error_url = request.build_absolute_uri(reverse("payment_result"))
        secret_key = "3328913f961f8b2bfb78000b3f9da02b"  # Fixme Todo: parametrize

        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)  # Fixme Todo: parametrize, secret key!
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        game_ids = [g.id for g in order._games.all()]

        # The form for the payment is hard-coded on the view.
        # just pass corresponding variables to the template
        return render(request, 'store/purchase.html', {'user': request.user,
                                                       'cart':  to_client_cart(game_ids),
                                                       'action': action,
                                                       'pid': pid,
                                                       'sid': sid,
                                                       'amount': amount,
                                                       'success_url': success_url,
                                                       'cancel_url': cancel_url,
                                                       'error_url': error_url,
                                                       'checksum': checksum})

    else:
        # This view only supports GET
        return HttpResponse(status=405, content="Invalid method.")


@login_required(login_url='login')
@user_passes_test(user_is_player, login_url='login')
def payment_result(request):
    """
    This view handles payment outcome. In case of success, user data is update according to the new games.
    In case of failure the user is redirected to teh purchase view, in which he can try again to pay.
    :param request:
    :return:
    """
    # Need to use transaction! #TODO FIXME

    # Note that accoring to the payment system specification we are breaking the rule of idempotent GET actions.
    if request.method == 'GET':
        # Check the payment data is correct
        pid = request.GET['pid']
        ref = request.GET['ref']
        result = request.GET['result']
        checksum = request.GET['checksum']

        # First check: authenticate the request
        sid = "italiancrea2016"  # Fixme Todo: parametrize
        secret_key = "3328913f961f8b2bfb78000b3f9da02b"  # Fixme Todo: parametrize

        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)  # Fixme Todo: parametrize, secret key!
        m = md5(checksumstr.encode("ascii"))
        checksum2 = m.hexdigest()

        if checksum != checksum2:
            messages.error(request, "Invalid checksum. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("cart"))

        # Second: verify PID exists
        order = None
        try:
            order = Order.objects.get(id=pid)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid OrderId specified. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("cart"))

        # Third: is this user allowed to manipulate this order?
        if order._player != request.user.profile:
            messages.error(request, "The order ID specified is not yours. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("cart"))

        # Fourth: is the order status consistent?
        if order.status != "pending":
            messages.error(request, "The order ID specified is not in the pending status. Please make another order.")
            return HttpResponseRedirect(redirect_to=reverse("cart"))

        # What about the result variable?
        if result not in ["success", "cancel", "error"]:
            messages.error(request, "The result parameter is unrecognized.")
            return HttpResponseRedirect(redirect_to=reverse("cart"))

        # Ok, now act according to the result
        if result == "success":
            for g in order._games.all():
                order._player._ownedGames.add(g)
            order._player.save()
            order.status = "success"
            order.paymentRef = ref
            order.paymentDate = datetime.datetime.now()
            order.save()

            # Empty the cart:
            request.session['cart_items'] = []

            return HttpResponseRedirect(redirect_to=reverse("thankyou"))

        elif result == "cancel":
            order.delete()
            messages.info(request,"The order has been canceled as requested.")
            return HttpResponseRedirect(redirect_to=reverse("cart"))

        elif result == "error":
            order.status = "error"
            messages.error(request,"There was an error processing the payment. Please try again!")
            return HttpResponseRedirect(redirect_to=reverse("order_details", kwargs={'order_id': pid}))


    else:
        # This view only supports GET
        return HttpResponse(status=405, content="Invalid method.")


@login_required(login_url='login')
@user_passes_test(user_is_player, login_url='login')
def thankyou(request):
    messages.success(request, "Thank you for your purchase. Enjoy the new game!")
    return HttpResponseRedirect(reverse('my_games'))


def to_client_cart(
        games_ids,        # type:list
        user=None         # type:User
):
    """
    Given an array of game_ids and an optional User object, this method
    gets all the info about the games into the list, by returning dictionary
    containing all the cart data.
    :param games_ids:
    :param user:
    :return:
    """
    res = {}
    res['games'] = []
    res['total'] = 0
    for id in games_ids:
        try:
            game = Game.objects.get(id=id)
            res['games'].append(game.to_json_dict(user=user))
            res['total'] += game.price
        except ObjectDoesNotExist:
            # Simply ignore. The game would not be added
            messages.error("One element of the cart was invalid.")
            continue
    return res


# ---------------------- DEVELOPERS' VIEWs ---------------------- #

@login_required(login_url='login')
@user_passes_test(user_is_developer, login_url='login')
def developer_games(request):
    # List all the games published by the developer and provide a form for adding a new one
    if request.method == 'GET':
        # Retrieve all the games of the current developer
        dev_games = Game.objects.filter(_developer=request.user.profile)

        response = {}
        games = []
        response['games'] = games
        for g in dev_games:
            tmp = g.to_json_dict()
            response['games'].append(tmp)

        # If the request is via Ajax, return json data representation
        if request.is_ajax():
            return JsonResponse(data=response)

        else:
            # Create a new form to be used in the template
            form = GameForm()
            return render(request, 'devzone/developed_games.html', {'form': form, 'user': request.user, 'games': games})
    elif request.method == 'POST':
        # Let's check if the form we got is OK. If there is something wrong, just return it to the view.
        # Otherwise proceed.
        form = GameForm(request.POST)
        if not form.is_valid():
            return render(request, "registration/register.html", {'form': form})
        else:
            # Regardless of the user's choice, update the publisher of this game.
            form.instance._developer = request.user.profile
            game = form.save()

            # Retrieve all the games of the current developer
            dev_games = Game.objects.filter(_developer=request.user.profile)
            games = [x.to_json_dict() for x in dev_games]

            messages.success(request=request, message='The game has been added successfully!')
            return render(request, 'devzone/developed_games.html', {'form': GameForm, 'user': request.user, 'games':games})
    else:
        return HttpResponse(status=405, content="Invalid method.")


@login_required(login_url='login')
@user_passes_test(user_is_developer, login_url='login')
def edit_game(request, game_id):
    if request.method == 'GET':

        # Retrieve the data from the db, starting from the game_id and use it to pre-populate the form
        # If the game does not belong to him, we send a 404 instead of a 401 error.
        game = get_object_or_404(Game, id=game_id, _developer=request.user.profile)
        form = GameForm(instance=game)
        return render(request, 'devzone/edit_game.html', {'form': form, 'user': request.user})

    elif request.method == 'POST':
        # Retrieve the data from the db, starting from the game_id and use it to pre-populate the form
        # If the game does not belong to him, we send a 404 instead of a 401 error.
        game = get_object_or_404(Game, id=game_id, _developer=request.user.profile)
        form = GameForm(request.POST, instance=game)

        if not form.is_valid():
            messages.error(request, "Please check the form errors and try egain.")
            return render(request, 'devzone/edit_game.html', {'form': form, 'user': request.user})
        else:
            if ('action' not in request.POST) or (request.POST['action'].lower() not in ['delete', 'save']):
                messages.error(request=request, message='Missing or invalid action parameter.')
                return HttpResponseRedirect(redirect_to=reverse('dev_games'))

            # Ok, perform the requested operation
            if request.POST['action'].lower() == 'save':
                game = form.save()
                messages.success(request=request, message='Game updated successfully.')
                return HttpResponseRedirect(redirect_to=reverse('dev_games'))
            elif request.POST['action'].lower() == 'delete':
                game.delete()
                messages.success(request=request, message='Game removed successfully.')
                return HttpResponseRedirect(redirect_to=reverse('dev_games'))
            else:
                messages.error(request=request, message='Missing or invalid action parameter.')
                return render(request, 'devzone/developed_games.html', {'form': form, 'user': request.user})

    else:
        return HttpResponse(status=405, content="Invalid method.")


@login_required(login_url='login')
@user_passes_test(user_is_developer, login_url='login')
def inventory(request):
    # This view returns a stand-alone HTML page in case the request is performed normally.
    # Otherwise, if ajax is detected, this view acts like a data provider, filtering
    # elements according to the filters specified by the client.
    if request.method=='GET':
        if not request.is_ajax():
            return render(request,"devzone/inventory.html")
        else:
            expected_params = ['period', 'from_date', 'to_date', 'games[]']

            # Check we have all the params
            for param in expected_params:
                if param not in request.GET:
                    return HttpResponse(status=400, content=json.dumps({'error','Missing parameter %s'%param}), content_type="text/json")

            # Check specific params are ok
            period = request.GET['period']
            from_date = request.GET['from_date']
            to_date = request.GET['to_date']
            input_games = request.GET.getlist('games[]')

            if period.lower() not in ['day', 'week', 'month']:
                return HttpResponse(status=400, content=json.dumps({'error','Invalid parameter period'}), content_type="text/json")

            start = None
            end = None
            try:
                start = datetime.datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                return HttpResponse(status=400, content=json.dumps({'error','Invalid parameter from_date'}), content_type="text/json")

            try:
                end = datetime.datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                return HttpResponse(status=400, content=json.dumps({'error', 'Invalid parameter to_date'}), content_type="text/json")

            if start > end:
                return HttpResponse(status=400, content=json.dumps({'error', 'from_date cannot be greater than to_date'}), content_type="text/json")

            response = {}
            line={}
            pie=[]
            line['labels'] = []
            line['dataset'] = []
            games = Game.objects.filter(id__in=input_games, _developer=request.user.profile)

            games_data = None
            ################# Build the Lines graph #################
            # Daily
            if period == 'day':
                games_data = Order.objects.filter(_games__id__in=games,
                                            status='success',
                                            orderDate__gte=start,
                                            orderDate__lte=end)

                data = games_data.values("orderDateYMD")\
                    .annotate(Count('id'))\
                    .order_by('orderDateYMD')

                # Format data to json result
                # data will contain a set of count__id-order_date values
                for d in data:
                    line['labels'].append((d['orderDateYMD']))
                    line['dataset'].append(d['id__count'])

            elif period == 'week':
                # To aggregate by week we need a WeekYear data into the model
                # Get all the orders aggregated by WeekYear
                startwy = start.strftime("%Y%U")
                endwy = end.strftime("%Y%U")

                games_data = Order.objects.filter(_games__id__in=games,
                                            status='success',
                                            orderDateYW__gte=startwy,
                                            orderDateYW__lte=endwy)

                data = games_data.values("orderDateYW")\
                    .annotate(Count('id'))\
                    .order_by('orderDateYW')

                # Format data to json result
                # data will contain a set of count__id-order_date values
                for d in data:
                    line['labels'].append(d['orderDateYW'])
                    line['dataset'].append(d['id__count'])

            elif period=='month':
                # To aggregate by week we need a WeekYear data into the model
                # Get all the orders aggregated by WeekYear
                startmy = start.strftime("%Y%m")
                endmy = end.strftime("%Y%m")

                games_data = Order.objects.filter(_games__id__in=games,
                                            status='success',
                                            orderDateYM__gte=startmy,
                                            orderDateYM__lte=endmy)

                data = games_data.values("orderDateYM")\
                    .annotate(Count('id'))\
                    .order_by('orderDateYM')

                # Format data to json result
                # data will contain a set of count__id-order_date values
                for d in data:
                    line['labels'].append(d['orderDateYM'])
                    line['dataset'].append(d['id__count'])

            response['line'] = line

            ################# Build the Pie graph #################
            # Simply drill down per game
            data = games_data.values("_games").annotate(Count('id'))
            for d in data:
                game_name = Game.objects.get(id=d['_games']).name
                pie.append({'label': game_name, 'value': d['id__count']})

            response['pie'] = pie

            return JsonResponse(data=response)

    else:
        return HttpResponse(status=405, content="Invalid method.")

