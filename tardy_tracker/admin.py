from django.contrib import admin

# Register your models here.
from tardy_tracker.models import User, Course, CheckIn


admin.site.register(User)
admin.site.register(Course)
admin.site.register(CheckIn)