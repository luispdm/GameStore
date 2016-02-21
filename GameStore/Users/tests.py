# Create your tests here.
from django.test import TestCase
from Users.models import Profile
from django.contrib.auth.models import User


class ModelsTest(TestCase):

    """
    Luigi
    Testing creation and update of Profile objects.
    """
    def testProfile(self):
        self.us1 = User.objects.create(username="user1", password="12345678", email="xx@gmail.com")
        user1 = Profile.objects.create(user=self.us1, activationToken="5bc8d00c-52b2-4dc0-9b47-b5920248de39")

        # Test creation
        self.assertEqual(user1.__str__(), 'user1')
        self.assertEqual(user1.user.password, '12345678')
        self.assertEqual(user1.activationToken, "5bc8d00c-52b2-4dc0-9b47-b5920248de39")
        self.assertEqual(user1.user.email, 'xx@gmail.com')

        # Test update
        user1.user.username = "user7"
        self.assertEqual(user1.__str__(), "user7")
        user1.user.password = "00000000"
        self.assertEqual(user1.user.password, "00000000")
        user1.activationToken = "0204e88f-fa44-4a92-87e4-9e0cdd0e416b"
        self.assertEqual(user1.activationToken, "0204e88f-fa44-4a92-87e4-9e0cdd0e416b")
        user1.user.email = "email@gmail.com"
        self.assertEqual(user1.user.email, "email@gmail.com")