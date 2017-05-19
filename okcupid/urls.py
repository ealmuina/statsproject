from django.conf.urls import url

from okcupid import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
