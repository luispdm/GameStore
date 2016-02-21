from django.db import transaction
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import Group, User

# Inject social-user into db
@transaction.atomic
def map_social_user(backend, user, response, *args, **kwargs):
    # This is a view-in-the-middle in order to give to the logged in user same structure we gave to the
    # classic user. That means we are going to assign a profile to it.
    # However we should check for email uniqueness and so on.
    # This function will be inserted into the pipeline of authentication about python-social-auth
    # We only support facebook, at the moment
    if backend.name == 'facebook':
        if not Profile.objects.filter(user=user).exists():
            # Create the profile
            p=Profile.objects.create(user=user, activationToken="NOT_NEEDED_FACEBOOK")
            p._ownedGames=[]
            p.save()

            # Assign groups to the user
            players = Group.objects.get(name='players')
            players.user_set.add(p.user)

    # We always return none
    return {}
