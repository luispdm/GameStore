from django.shortcuts import render
from Store.models import Game
from .models import PlayedMatch, SavedGame
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MessageForm, MessageScoreForm, MessageLoadForm, MessageSaveForm
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.decorators import user_passes_test
from common.utils import user_is_developer, user_is_player
from django.core.urlresolvers import reverse


@login_required(login_url='login')
@user_passes_test(user_is_player, login_url='login')
def play_game(request, game_id):
    """
    This view takes care of handling the gaming part of the website. If the request comes as a GET, we serve the page
    to play to the specified game.
    However, the web-page may interact to save/load/load_request messages with us. For this we use the POST handler.
    Note that for the "LOAD_REQUEST" seems to be idempotent, but it is not. It increases some "popularity" counter
    in our system, so it makes perfect sense to handle this request by POST. We do not enforce POST to be performed
    via Ajax, but we'll only return JSON data via the post.
    For every request, we also check the user owns the game, before doing everything else.
    :param request:
    :param game_id:
    :return:
    """

    # Retrieve info about the game specified or kick the user out
    game = get_object_or_404(Game, id=game_id)
    perm = request.user.profile._ownedGames.filter(id=game_id).exists()
    if not perm:
        messages.error(request, "You do not own this game. Why don't you buy it?")
        return HttpResponseRedirect(reverse("list_games"))

    # Ok the user seems to be allowed to play this game, get the remote url and serve it into the template, alongside
    # basic game info for GET, otherwise handle any POST message, if any.
    if request.method == 'GET':
        return render(request,"gamearena/play_game.html", {'game': game.to_json_dict(request.user.profile),
                                                           'remote_server': game.url})

    elif request.method == 'POST':
        # It doesn't matter what kind of request the page has made, our response will be something aligning to the
        # following. In case one or more error are found, we will return them into the error field. So the page
        # can easily guess if an error has occurred by simply checking error is null. If the response is supposed
        # to contain a body, we'll put that into the result field. Note that if result is null, it does not mean we
        # got an error, in fact it only means we have nothing to say to the page. Also we will return a 400 code
        # in case of error or 200 code upon success.
        resp = {
            "error": None,
            "result": None
        }

        # Parse the message type and basic sanitizing
        form = MessageForm(request.POST)
        if not form.is_valid():
            resp['error'] = form.errors
            return JsonResponse(status=400, data=resp)

        # Parse the specific message and handle it.
        if form.cleaned_data['messageType'] == 'SCORE':
            # The player has finished a match and there is a score notification.
            # let's save it on the db.
            scoreForm = MessageScoreForm(request.POST)
            if not scoreForm.is_valid():
                resp['error'] = scoreForm.errors
                return JsonResponse(status=400, data=resp)

            PlayedMatch.objects.create(score=scoreForm.cleaned_data['score'],
                                       playedDate=datetime.datetime.utcnow(),
                                       _player=request.user.profile,
                                       _game=game)

            return JsonResponse(status=201, data=resp)

        elif form.cleaned_data['messageType'] == 'SAVE':
            # The player wants to save the current game status
            # let's save it on the db.
            saveForm = MessageSaveForm(request.POST)
            if not saveForm.is_valid():
                resp['error'] = saveForm.errors
                return JsonResponse(status=400, data=resp)

            saving = SavedGame.objects.update_or_create(_player=request.user.profile, _game=game)[0]
            saving.savedDate = datetime.datetime.utcnow()
            saving.status = saveForm.cleaned_data['gameState']
            # settings??
            saving.save()
            return JsonResponse(status=201, data=resp)

        elif form.cleaned_data['messageType']=='LOAD_REQUEST':
            loadForm = MessageLoadForm(request.POST)
            if not loadForm.is_valid():
                resp['error'] = loadForm.errors
                return JsonResponse(status=400, data=resp)

            saving = SavedGame.objects.filter(_player=request.user.profile,
                                     _game=game).order_by("-savedDate")

            if saving.exists():
                resp['result'] = saving[0].status
                return JsonResponse(status=200, data=resp)
            else:
                resp['result'] = None
                resp['error'] = "There are no saved games."
                return JsonResponse(status=200, data=resp)

        else:
            resp['error'] = "Invalid message type."
            return JsonResponse(status=400, data=resp)

    else:
        return HttpResponse(status=405, content="Invalid method specified.")


# This view is public: it does not require any authentication
def leader_board(request):
    """
    The leaderboard works with the Ajax service provided for the game navigation.
    Once served the "static page", javascript will take care of the rest.
    :param request:
    :return:
    """
    return render(request, "gamearena/leaderboard.html", {'user': request.user})


# This view is public: it does not require any authentication
def leader_board_game(request, game_id):
    """
    This view is invoked by Javascript AJAX: it return Json Data to display the top 10
    players-score for the given game_id.
    :param request:
    :param game_id:
    :return:
    """

    # TODO: Possible improvement: serve the page both as JSON (on ajax) and as RAW HTML to be embeded with iFrames/DIVs

    game = None
    try:
        game = Game.objects.get(id=game_id)
    except ObjectDoesNotExist:
        return JsonResponse(status=404, data={"error":"Game id does not exist."})

    scores = PlayedMatch.objects.filter(_game=game).values('_player__user__username').annotate(score=Max('score'))[0:10]

    result = {}
    result['game'] = game.to_json_dict(user=request.user)
    result['scores'] = [{'player':s['_player__user__username'], 'score':s['score']} for s in scores]

    return JsonResponse(data=result)


def close_popup(request):
    # Simply closes the window
    return render(request, "gamearena/closepopup.html")