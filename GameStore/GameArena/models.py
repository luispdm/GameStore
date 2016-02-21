from Users.models import Profile
from django.db import models
from django.utils import timezone


# This file contains the basic structures of a saved game and a played match
class PlayedMatch(models.Model):
    score = models.FloatField(default=0)
    playedDate = models.DateTimeField(default=timezone.now)
    _player = models.ForeignKey('Users.Profile')
    _game = models.ForeignKey('Store.Game')

    def __str__(self):
        return str(self.score)

    def to_json_dict(self):
        res = {}
        res['score'] = self.score
        res['playedDate'] = str(self.playedDate)
        res['game'] = self._game.name
        res['player'] = self._player.user.username

        return res

class SavedGame(models.Model):
    status = models.TextField()
    savedDate = models.DateTimeField(default=timezone.now)
    settings = models.TextField()
    _player = models.ForeignKey('Users.Profile')
    _game = models.ForeignKey('Store.Game')

    def __str__(self):
        return str(self.status)
