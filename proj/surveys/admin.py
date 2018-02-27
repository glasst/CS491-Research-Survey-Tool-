from django.contrib import admin

# Register your models here.
from .models import  Profile, Survey, Question, MCQuestion, TEQuestion, CBQuestion, Response

admin.site.register(MCQuestion)
admin.site.register(TEQuestion)
admin.site.register(CBQuestion)
admin.site.register(Survey)
admin.site.register(Response)
admin.site.register(Profile)
admin.site.register(Question)
