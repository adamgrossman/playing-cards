from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=True)

    def __unicode__(self):
        return u"{}: {} {}".format(self.username, self.first_name, self.last_name)


class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name="student_courses")
    teacher = models.ForeignKey(User, related_name="teacher_courses")
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __unicode__(self):
        return u"{}".format(self.name)


class CheckIn(models.Model):
    student = models.ForeignKey(User, related_name="check_ins")
    course = models.ForeignKey(Course, related_name="check_ins")
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u"{} {} {}".format(self.course, self.student, self.date)