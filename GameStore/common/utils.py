from django.contrib.auth.models import Group
import uuid


def is_uuid_valid(uuid_str):
    try:
        val = uuid.UUID(uuid_str, version=4)
        return True
    except:
         return False


def user_is_developer(user):
    # If the user is not logged, return false
    if not user.is_authenticated():
        return False

    # Otherwise check if he's into the developers group
    return user.groups.filter(name__in=['developers']).exists()


def user_is_player(user):
    # If the user is not logged, return false
    if not user.is_authenticated():
        return False

    # Otherwise check if he's into the developers group
    return user.groups.filter(name__in=['players']).exists()