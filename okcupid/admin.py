# Register your models here.
from django.contrib import admin

from okcupid.models import UserProfile, Gender, Question, Opinion, SentQuestion

admin.site.register(UserProfile)
admin.site.register(Gender)
admin.site.register(Question)
admin.site.register(Opinion)
admin.site.register(SentQuestion)
