from django.conf.urls import url
from .views import RegisterKey,Sign, HomePage, PostOne, DeleteOne, UpdateOne, GetList,List, Detail, Delete, Patch, GetOne, ForgotKey, MailKey

urlpatterns=[

    # Home Page
    url(r'^$',HomePage),


    # Generating django forms
    url(r'^registerkey/$',RegisterKey),
    url(r'^postone/$', PostOne),
    url(r'^getlist/$', GetList),
    url(r'^getone/$', GetOne),
    url(r'^deleteone/$', DeleteOne),
    url(r'^updateone/$', UpdateOne),
    url(r'^getfkey/', ForgotKey),


    # for saving users credential in db
    url(r'^sign$', Sign),


    # made as per the instruction given in the article
    url(r'^list/$',List),
    url(r'^detail/$', Detail),

    # to handle request made by django forms
    url(r'^delete/$', Delete),
    url(r'^patch/$', Patch),
    url(r'^mailkey/', MailKey)

]