from django.test import TestCase
from GameArena.models import PlayedMatch
from GameArena.models import SavedGame
from Users.models import Profile
from Store.models import Game
from Store.models import Category
from django.contrib.auth.models import User, Group
"""
Luigi
Testing creation/update of SavedGame and PlayedMatch models (creation of Profile and Game needed in order to see the
test works).
"""


class ModelsTest(TestCase):

    def testPlayedMatch(self):
        us1 = User.objects.create(username="profile1", password="12345678", email="xx@gmail.com")
        category1 = Category.objects.create(name="Action")
        category2 = Category.objects.create(name="Sports")
        profile1 = Profile.objects.create(user=us1, activationToken="5bc8d00c-52b2-4dc0-9b47-b5920248de39")
        group1 = Group.objects.create(name="developers")
        group1.user_set.add(profile1.user)

        game1 = Game.objects.create(name="Clash of Clans", description="No descr", url="http://www.google.com", price=
                                     3, _category=category1, popularity=0, logo="http://www.image.com",
                                    _developer=profile1)
        us2 = User.objects.create(username="profile2", password="12345678", email="xxxx@gmail.com")
        profile2 = Profile.objects.create(user=us2, activationToken="5bc8d00c-52b2-4dc0-9b47-b5920248de39")
        group1.user_set.add(profile2.user)
        game2 = Game.objects.create(name="Fifa 16", description="No descr", url="http://www.yahoo.com", price=
                                    3, _category=category2, popularity=0, logo="http://www.image.com",
                                    _developer=profile2)

        playedmatch1 = PlayedMatch.objects.create(score=500, _player=profile1, _game=game1)

        # Test creation
        self.assertEqual(playedmatch1.score, 500)
        self.assertEqual(playedmatch1._game, game1)
        self.assertEqual(playedmatch1._player, profile1)

        # Test update
        playedmatch1.score = 5000
        self.assertEqual(playedmatch1.score, 5000)
        playedmatch1._player = profile2
        self.assertEqual(playedmatch1._player, profile2)
        playedmatch1._game = game2
        self.assertEqual(playedmatch1._game, game2)

    def testSavedGame(self):
        us1 = User.objects.create(username="profile1", password="12345678", email="xx@gmail.com")
        category1 = Category.objects.create(name="Action")
        category2 = Category.objects.create(name="Sports")
        profile1 = Profile.objects.create(user=us1, activationToken="5bc8d00c-52b2-4dc0-9b47-b5920248de39")
        group1 = Group.objects.create(name="developers")
        group1.user_set.add(profile1.user)

        game1 = Game.objects.create(name="Clash of Clans", description="No descr", url="http://www.google.com", price=
                                     3, _category=category1, popularity=0, logo="http://www.image.com",
                                    _developer=profile1)
        us2 = User.objects.create(username="profile2", password="12345678", email="xxxx@gmail.com")
        profile2 = Profile.objects.create(user=us2, activationToken="5bc8d00c-52b2-4dc0-9b47-b5920248de39")
        group1.user_set.add(profile2.user)
        game2 = Game.objects.create(name="Fifa 16", description="No descr", url="http://www.yahoo.com", price=
                                    3, _category=category2, popularity=0, logo="http://www.image.com",
                                    _developer=profile2)

        savedgame1 = SavedGame.objects.create(status="LOAD", settings="Resolution", _player=profile1, _game=game1)

        # Test creation
        self.assertEqual(savedgame1.status, "LOAD")
        self.assertEqual(savedgame1.settings, "Resolution")
        self.assertEqual(savedgame1._player, profile1)
        self.assertEqual(savedgame1._game, game1)

        # Test update
        savedgame1.status = "SAVE"
        self.assertEqual(savedgame1.status, "SAVE")
        savedgame1.settings = "NOSETTINGS"
        self.assertEqual(savedgame1.settings, "NOSETTINGS")
        savedgame1._player = profile2
        self.assertEqual(savedgame1._player, profile2)
        savedgame1._game = game2
        self.assertEqual(savedgame1._game, game2)
