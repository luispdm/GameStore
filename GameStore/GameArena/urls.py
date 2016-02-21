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

urlpatterns = [
    # Registration is the only view that django auth does not provide natively, so we use ours.
    url(r'^play/(?P<game_id>[0-9]+)/$', views.play_game, name='play_game'),
    url(r'^leader_board_game/(?P<game_id>[0-9]+)/$', views.leader_board_game, name='leader_board_game'),
    url(r'^leader_board/$', views.leader_board, name='leader_board'),
    url(r'close_popup/$', views.close_popup, name='close_popup'),
]