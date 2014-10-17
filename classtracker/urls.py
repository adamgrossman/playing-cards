from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tardy_tracker.views.base', name='base'),
    url(r'^home/$', 'tardy_tracker.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    #url(r'^checkin/$', 'tardy_tracker.views.checkin', name='checkin'),

    url(r'^checkin/$', 'tardy_tracker.views.new_check_in', name='check_in'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^teacher/$', 'tardy_tracker.views.teacher_home', name='teacher_home'),

    url(r'^course/(?P<course>.+)/$', 'tardy_tracker.views.course_details', name='course_details'),
)
