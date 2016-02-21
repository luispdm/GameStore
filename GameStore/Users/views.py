import uuid
from django.db import transaction, IntegrityError
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from common.utils import is_uuid_valid
from .forms import RegistrationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required

# This string makes the email sender to emulate the email by printing it on STDOUT.
settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Alberto: registration is a serious matter. We would like to provide transaction protection
# so if the mail is not sent or if there is a problem during registration we can always recover
@transaction.atomic
def register(request):
    """
    This view is invoked directly by django when the user tries to register.
    Once completed, the user is not yet active: he must confirm his own email address.
    :param request:
    :return:
    """
    if request.user.is_authenticated():
        messages.warning(request, "You are already logged in.")
        return HttpResponseRedirect(reverse('home'))  # FIXME: redirect to account info not at home

    if request.method == 'POST':
        # We assume post is used for bounded forms, so the data has to be processed
        form = RegistrationForm(request.POST)

        # We don't need to check for uniqueness of username & email
        # because it is guaranteed by the model.
        if not form.is_valid():
            return render(request, "registration/register.html", {'form': form})
        else:
            # Set the user activation to false: user must activate himself to log into the system.
            form.instance.is_active = False
            new_user = form.save()

            # Generate the player profile, link it to the User and save it
            actToken = uuid.uuid4()
            p = Profile.objects.create(user=new_user, activationToken=actToken)
            p.save()

            # If the user has applied to be a developer
            if form.cleaned_data["applyAsDeveloper"]:
                devs = Group.objects.get(name='developers')
                devs.user_set.add(p.user)
            else:
                # Otherwise he'll be jsut a player
                players = Group.objects.get(name='players')
                players.user_set.add(p.user)

            # We now send the activation email to the user and redirect him to the activation page.
            mail_title = 'Confirm your subscription!'
            message = 'Please visit the following link to complete your subscription: .... %s' % \
                      request.build_absolute_uri(reverse(viewname='activate', args=(actToken,)))

            new_user.email_user(mail_title, message)

            # Redirect the user to the homepage and notify activation is needed
            messages.success(request=request, message='You have correctly registered to our portal. '
                                                      'An activation mail has been sent to your email account. '
                                                      'To log in, you will need to activate yourself by clicking '
                                                      'the activation link provided into that email.')
            return HttpResponseRedirect(reverse("home"))

    elif request.method == 'GET':
        # When invoked with GET method, this view prints the registration page.
        form = RegistrationForm()

        return render(request, "registration/register.html", {
            'form': form,
        })


# Note: this does not require any authentication.
def activate(request, activationCode=None):
    """
    #Alberto#
    This view handles activation by users. It only serves GET requests because we plan to use simple activation
    link to enable user activation. Either on success or failure, the user is redirected to the home page
    and appropriate message is set. It is up to the template to display any error that has occurred here.
    Please note that an user may only activate himself once.
    :param request:
    :param activationCode:
    :return:
    """
    if request.method == 'GET':

        if not is_uuid_valid(activationCode):
            messages.error(request=request, message='The activation id provided is invalid.')
        else:
            p = None
            try:
                # We handle the transaction manually. Note that we should not catch any exception
                # inside the atomic block. We can only catch and handle exception externally,
                # so the atomic middleware takes care fo rolling back.
                with transaction.atomic():
                    # Get an user by its activation code and activate him if necessary
                    p = Profile.objects.get(activationToken=activationCode)
                    if p.user.is_active:
                        # The user was already active!
                        messages.error(request=request, message='Your account has already been activated.')
                    else:
                        p.user.is_active = True
                        p.user.save()
                        messages.success(request=request, message='You have correctly activated your account!')

            except ObjectDoesNotExist:
                messages.error(request=request, message='There was a problem during activation. Please try again.')

        return HttpResponseRedirect(redirect_to=reverse("home"))


# The standard Django login view does not check whether the user is already logged in or not.
# So we add this view in the miggle in order to redirect the user to the list_games when he's
# logged.
def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account'))
    else:
        return login(request, template_name='registration/login.html')


def social_error(request):
    """
    If there was a problem using standard social authentication, redirect the user to the
    login page in order to let him try again.
    :param request:
    :return:
    """
    messages.error(request, "There was a problem using Social Authentication. ")
    return HttpResponseRedirect(reverse('login'))

@login_required(login_url='login')
def account(request):
    return render(request, "account/account.html", {'user':request.user})