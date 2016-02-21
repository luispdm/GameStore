from Store.models import Order
import datetime
from random import randint
from Users.models import Profile

import django

def update(username, day, month, year):
    i = Order.objects.get(_player__user__username=username)
    i.orderDate = datetime.datetime.strptime(("%d %d %d" % (day, month, year)), "%d %m %Y")
    i.paymentDate = i.orderDate  # change paymentDate
    i.orderDateY = i.orderDate.strftime("%Y")
    i.orderDateYM = i.orderDate.strftime("%Y%m")
    i.orderDateYW = i.orderDate.strftime("%Y%U")
    i.orderDateYMD = i.orderDate.strftime("%Y%m%d")
    i.save()


if __name__ == '__main__':
    django.setup()
    update('user1', 10, 12, 2015)
    update('user2', 28, 11, 2015)
    update('user3', 15, 12, 2015)
    update('user58', 25, 11, 2015)