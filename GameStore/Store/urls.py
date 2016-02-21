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
from . import views

urlpatterns = [
    # Public
    url(r'^$', views.list_games, name='list_games'),

    # For Logged users=>Players
    url(r'^my_games/$', views.my_games, name='my_games'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'^order_details/(?P<order_id>[a-zA-Z0-9]+)/$', views.order_details, name='order_details'),
    url(r'^payment_result/$', views.payment_result, name='payment_result'),
    url(r'^thank_you/$', views.thankyou, name='thankyou'),

    # For Logged users=>Developers
    url(r'^devzone/games/$', views.developer_games, name='dev_games'),
    url(r'^devzone/edit_game/(?P<game_id>[0-9]+)/$', views.edit_game, name='edit_game'),
    url(r'^devzone/inventory/$', views.inventory, name='inventory'),
]