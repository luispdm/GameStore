"""GameStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, \
    password_reset_done, password_reset_confirm, password_reset_complete
from . import views

# Alberto: this is used by django to redirect the user after a successful login. In this case we redirect to the home.
# Note: this should always match a NAMED URL PATTERN. Hard-coding this parameter is not a good idea.
settings.LOGIN_REDIRECT_URL = "home"

# TODO: customize all other settings, i.e. https://docs.djangoproject.com/en/1.9/ref/settings/

urlpatterns = [
    # Registration is the only view that django auth does not provide natively, so we use ours.
    url(r'^register$', views.register, name='register'),

    # Route the user to its main administration area
    url(r'^manage$', views.account, name='account'),

    # Alberto: instead of relying on default django urls for auth, we customize them
    url(r'^login/$',
        views.custom_login,
        name='login'),

    url(r'^logout/$',
        logout,
        {'template_name':'account/logged_out.html'},
        name='logout'),

    url(r'^password_change/$',
        password_change,
        {'template_name':'account/password_change_form.html'},
        name='password_change'),

    url(r'^password_change/done/$',
        password_change_done,
        {'template_name': 'account/password_change_done.html'},
        name='password_change_done'),

    url(r'^password_reset/$',
        password_reset,
        {'template_name': 'account/password_reset_form.html'},
        name='password_reset'),

    url(r'^password_reset/done/$',
        password_reset_done,
        {'template_name': 'account/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {'template_name': 'account/password_reset_confirm.html'},
        name='password_reset_confirm'),

    url(r'^reset/done/$',
        password_reset_complete,
        {'template_name': 'account/password_reset_complete.html'},
        name='password_reset_complete'),

    # Facebook login
    # Not really needed! See settings.py
    url(r'^social_error/$',
        views.social_error,
        name='social_error'),

    # Activation is not natively supported by django. We have to implement it.
    url(r'^activate$',views.activate, name='activate'),
    url(r'^activate/(?P<activationCode>[a-zA-Z0-9\-]{36})/$', views.activate, name='activate'),
]