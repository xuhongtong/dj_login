from django.conf.urls import url
from app_login import views
urlpatterns=[
    url(r'^index/$',views.index),
    url(r'^login/$',views.login),
    url(r'^register/$',views.register),
    url(r'^logout/$',views.logout),
    url(r'^confirm/$',views.user_confirm)
]
