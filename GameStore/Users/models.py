from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
    activationToken = models.CharField(max_length=36)

    _ownedGames = models.ManyToManyField('Store.Game', default=None, blank=True)

    """
    The default behavior of the ManyToMany states that if the instance is deleted, the object can't access to it anymore
    """

    @property
    def is_player(self):
        return self.user.groups.filter(name='players').exists()

    @property
    def is_developer(self):
        return self.user.groups.filter(name='developers').exists()

    def __str__(self):
        return str(self.user.username)
