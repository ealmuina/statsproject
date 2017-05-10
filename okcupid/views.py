from django.http import HttpResponse

from okcupid.models import *


def index(request):
    harry = UserProfile.objects.get(user__username='harry')
    hermione = UserProfile.objects.get(user__username='hermione')
    return HttpResponse(str(UserProfile.match_percentage(harry, hermione)))
