from django.conf.urls import url, include

from okcupid import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^register', views.RegsiterView.as_view(), name='register'),
    url(r'^send_question', views.SendQuestionView.as_view(), name='send_question'),
    url(r'^send_opinion', views.OpinionView.as_view(), name='send_opinion'),
    url(r'^matches', views.MatchesView.as_view(), name='matches_list'),

]
