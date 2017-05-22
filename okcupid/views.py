from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from okcupid.forms import UserForm, UserProfileForm
from okcupid.models import *


class IndexView(TemplateView):
    template_name = 'okcupid/index.html'


class RegsiterView(View):
    def get(self, request):
        context = {
            'title': 'Registration',
            'bread_crumbs': ['Home', 'Registration']
        }
        return render(request, 'registration/register.html', context)

    def post(self, request):
        context = {'message': []}
        if request.POST['terms'] != 'checked':
            context['message'].append("Necesita aceptar lso terminos para poder registrarse")
        if request.POST['password'] != request.POST['password_check']:
            context['message'].append("Las cotraseñas no coinciden")
        if len(context['message']) > 0:
            render(request, 'registration/register.html')

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if (user_form.is_valid() and profile_form.is_valid()):
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            # user.first_name = request.POST['first_name']
            # user.last_name = request.POST['last_name']
            # profile = UserProfile(user=user)


class SendQuestionView(LoginRequiredMixin, View):
    def post(self, request):
        q = SentQuestion(question=request.POST['question'])
        q.sender_id = request.user.id
        q.save()
        return HttpResponse('Question sent')


class OpinionView(LoginRequiredMixin, View):
    def post(self, request):
        op = Opinion(text=request.POST['text'])
        op.user_id = request.user.id
        op.save()
        return HttpResponse('Opinion sent')


class MatchesView(LoginRequiredMixin, View):
    def get(self, request):
        # TODO: Hacer la paginacion
        context = {
            'title': 'Matches',
            'bread_crumbs': ['Dashboard', 'Matches'],
            'matches': MatchEvaluation.matches_for(request.user.id)
        }
        return render(request, 'okcupid/matches.html', context)
