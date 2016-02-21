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
from django.conf.urls import url, include
from . import views

urlpatterns = [
    # Map the API list

    # mapped to /v1
    url(r'^$', views.v1, name='v1'),

    # mapped to /v1/games
    url(r'^games/$', views.games, name='games'),

    # mapped to /v1/games/<game_id>
    url(r'^games/(?P<game_id>[0-9]+)/$', views.game, name='game'),

    # mapped to /v1/categories
    url(r'^categories/$', views.categories, name='categories'),

    # mapped to /v1/categories/<category_id>
    url(r'^categories/(?P<category_id>[0-9]+)/$', views.category, name='category'),
]