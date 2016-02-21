from Users.models import Profile
# from Users.models import Developer
from django.contrib.auth.models import AnonymousUser, User
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


# Game, Category and Purchase models. Since categories are a preset, it's easier developing a category.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def to_json_dict(self):
        res = {
            'id': self.id,
            'name': self.name}
        return res

    def __str__(self):
        # Alberto: Luigi pay attention! You MUST return a string, not an integer. I've spent
        # 20 minutes to figure this out.
        #return self.id
        return str(self.name)


class Game(models.Model):
    """
    Developer can delete a Game => an Order shouldn't be affected, but PlayedMatch and SavedGame have a ForeignKey
    on Game => ON CASCADE DELETE
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField()
    url = models.URLField(unique=True)
    price = models.FloatField(default=0)
    publicationDate = models.DateTimeField(default=timezone.now)
    logo = models.URLField(default="http://www.yourimage.com")  # URL of the image of the game
    popularity = models.IntegerField(default=0)
    _category = models.ForeignKey('Category', null=False)
    _developer = models.ForeignKey('Users.Profile', null=False)

    def __str__(self):
        return str(self.name)

    def to_json_dict(self, user=None):
        res = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'url': reverse("play_game", kwargs={'game_id': self.id}),
            'price': self.price,
            'publicationDate': str(self.publicationDate),
            'category_id': self._category.id,
            'category': self._category.name,
            'popularity': self.popularity,
            'logo': self.logo,
            'developer': self._developer.user.username,
            'leaderboard_url': reverse("leader_board_game", kwargs={'game_id': self.id})
        }

        # Let's emulate a middleware over here...
        if user is not None and isinstance(user, User) and user.is_authenticated():
            owned = False
            o = user.profile._ownedGames.filter(id=self.id)
            if o.count()>0:
                res['owned'] = True
            else:
                res['owned'] = False

        return res


def get_default_yw():
    return timezone.now().date().strftime("%Y%U")


def get_default_ym():
    return timezone.now().date().strftime("%Y%m")


def get_default_y():
    return timezone.now().date().strftime("%Y")

def get_default_ymd():
    return timezone.now().date().strftime("%Y%m%d")


class Order(models.Model):
    # PaymentId
    id = models.AutoField(primary_key=True)

    # Buyer
    _player = models.ForeignKey('Users.Profile', null=False)

    # Items bought
    _games = models.ManyToManyField('Game', default=None, blank=True)

    # Represents the total of the order
    total = models.FloatField(default=0, null=False)

    # When the order was submitted
    orderDate = models.DateTimeField(default=timezone.now, null=False)
    orderDateYMD = models.CharField(max_length=8, default=get_default_ymd, null=False)
    orderDateYW = models.CharField(max_length=6, default=get_default_yw, null=False)
    orderDateYM = models.CharField(max_length=6, default=get_default_ym, null=False)
    orderDateY = models.CharField(max_length=4, default=get_default_y, null=False)

    # When the order was paid (if it was)
    paymentDate = models.DateTimeField(default=None, null=True)

    # Reference provided by the payment system
    paymentRef = models.IntegerField(null=True, default=0) # TODO: check this. What kind of refs are we expecting? Validation? Unique?

    # can be pending/success/error/cancel
    status = models.CharField(max_length=10, null=False, default="pending")


    def __str__(self):
        #TODO: what should we return when printing an order?
        return str(self.total)
