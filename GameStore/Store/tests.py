from django.test import TestCase
from Store.models import Game
from Store.models import Category
from Store.models import Order
from Users.models import Profile
from django.contrib.auth.models import User, Group
from django.db.models import Sum
"""
Luigi
Testing creation/update of Category, Game and Order models
(creation of Profile needed in order to see the test works).
"""


class ModelsTest(TestCase):

    def testCategory(self):
        category1 = Category.objects.create(name="Action")

        # Test creation
        self.assertEqual(category1.name, "Action")

        # Test update
        category1.name = "RPG"
        self.assertEqual(category1.name, "RPG")

    def testGame(self):
        us1 = User.objects.create(username="profile1", password="12345678", email="xx@gmail.com")
        category1 = Category.objects.create(name="Action")
        category2 = Category.objects.create(name="Sports")
        profile1 = Profile.objects.create(user=us1, activationToken="5bc8d00c-52b2-4dc0-9b47-b5920248de39")
        group1 = Group.objects.create(name="developers")
        group1.user_set.add(profile1.user)

        game1 = Game.objects.create(name="Clash of Clans", description="No descr", url="http://www.google.com", price=
                                     3, _category=category1, popularity=0, logo="http://www.image.com",
                                    _developer=profile1)
        game2 = Game.objects.create(name="Fifa 16", description="No descr", url="http://www.yahoo.com", price=
                                    3, _category=category2, popularity=0, logo="http://www.image.com",
                                    _developer=profile1)
        profile1._ownedGames.add(game1)
        profile1._ownedGames.add(game2)

        # Test creation
        self.assertEqual(profile1._ownedGames.get(pk=game1.pk), game1)
        self.assertEqual(profile1._ownedGames.get(pk=game2.pk), game2)
        self.assertEqual(game1.name, "Clash of Clans")
        self.assertEqual(game1.description, "No descr")
        self.assertEqual(game1.url, "http://www.google.com")
        self.assertEqual(game1.price, 3)
        self.assertEqual(game1.popularity, 0)
        self.assertEqual(game1._category, category1)
        self.assertEqual(game1.logo, "http://www.image.com")
        self.assertEqual(game1._developer, profile1)

        # Test update
        profile1._ownedGames.remove(game1)
        z = profile1._ownedGames.all()
        self.assertEqual(z.count(), 1)

        game1.name = "CC"
        self.assertEqual(game1.name, "CC")
        game1.description = "Hello"
        self.assertEqual(game1.description, "Hello")
        game1.url = "http://www.facebook.com"
        self.assertEqual(game1.url, "http://www.facebook.com")
        game1.price = 7
        self.assertEqual(game1.price, 7)
        game1.popularity = 4
        self.assertEqual(game1.popularity, 4)
        game1._category = category2
        self.assertEqual(game1._category, category2)
        game1.logo = "http://www.logonumberone.com"
        self.assertEqual(game1.logo, "http://www.logonumberone.com")

    def testOrder(self):
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
                                    5, _category=category2, popularity=0, logo="http://www.image.com",
                                    _developer=profile2)

        order1 = Order.objects.create(_player=profile1,  status="success", paymentRef=502)
        order1._games.add(game1)
        order1._games.add(game2)
        for x in order1._games.all():   # calculating the final price of the order
            order1.total += x.price

        # Test creation
        self.assertEqual(order1.total, order1._games.all().aggregate(Sum('price'))['price__sum'])
        self.assertEqual(order1._games.get(pk=game1.pk), game1)
        self.assertEqual(order1._games.get(pk=game2.pk), game2)
        self.assertEqual(order1._player, profile1)
        self.assertEqual(order1.paymentRef, 502)
        self.assertEqual(order1.status, "success")

        # Test update
        order1._games.remove(game1)
        z = order1._games.all()
        self.assertEqual(z.count(), 1)

        order1.total -= game1.price
        self.assertEqual(order1.total, game2.price)
        order1._player = profile2
        self.assertEqual(order1._player, profile2)
        order1.paymentRef = 333
        self.assertEqual(order1.paymentRef, 333)
        order1.status = "cancel"
        self.assertEqual(order1.status, "cancel")

