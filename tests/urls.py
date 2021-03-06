from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import render
from tests.models import Lesson


def lessons(request):
    lessons = Lesson.objects.all()
    return render(request, 'tests/lessons.html', {'lessons': lessons})


urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
    url(r'^lessons/$', lessons, name='lessons')
)
