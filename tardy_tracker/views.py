import datetime
import json
from django.db.models import Count

# from django.http import HttpResponse
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
#
# from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from tardy_tracker.models import Course, CheckIn, User

def base(request):
    return render(request, 'base.html')

def teacher_home(request):
    courses = Course.objects.filter(teacher=request.user)
    data = {
        'courses': courses
    }
    return render(request, 'teacher_home.html', data)


def student_home(request):
    courses = Course.objects.filter(students=request.user)
    data = {
        'courses': courses
    }
    return render(request, 'student_home.html', data)


def home(request):
    if request.user.is_student:
        current_time = datetime.datetime.now().time()
        today = datetime.datetime.now().date()
        has_checked_in = []
        courses = Course.objects.filter(students=request.user, start_time__lte=current_time, end_time__gte=current_time)
        course = Course.objects.get(name=courses[0])
        total = CheckIn.objects.filter(course=course).values('student').annotate(dcount=Count('student')).order_by('-dcount')[0]
        if courses:
            has_checked_in = CheckIn.objects.filter(student=request.user, course=courses[0], date=today)
        data = {
            'courses': courses,
            'has_checked_in': has_checked_in,
            'time': current_time,
            'total' : total['dcount']
        }
        print data
        return render(request, 'student_home.html', data)
    else:
        current_time = datetime.datetime.now().time()
        today = datetime.datetime.now().date()
        current_course = Course.objects.filter(teacher=request.user, start_time__lte=current_time, end_time__gte=current_time)
        current_status = []
        if current_course:
            for student in User.objects.filter(student_courses=current_course[0]):
                current_status.append({
                    'student': student.username,
                    'logged_in': CheckIn.objects.filter(student=student, course=current_course[0], date=today)
                })
        courses_today = Course.objects.filter(teacher=request.user)
        data = {
            'current_course': current_course,
            'courses_today': courses_today,
            'current_status': current_status
        }
        return render(request, 'teacher_home.html', data)

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

@csrf_exempt
def new_check_in(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        stu = (data['student']).lower()
        student = User.objects.get(username=stu)
        course = Course.objects.get(name=data['course'])
        check_in = CheckIn.objects.create(course=course, student=student)
        testcheckin = CheckIn.objects.filter(student=student, course=course).count()
        total = CheckIn.objects.filter(course=course).values('student').annotate(dcount=Count('student')).order_by('-dcount')[0]
        charts = CheckIn.objects.filter(student=student).values('course').annotate(dcount=Count('course'))
        charts_list = ValuesQuerySetToDict(charts)
        check_in_tot = total['dcount']
        print charts_list,'charts'
        data = {'count':'testcheckin','message':'already_in','checkin_total':check_in_tot,'chart_data':charts_list}
        print data,'data'
        #response = serializers.serialize('json', {data})
        response = json.dumps(data)
        return HttpResponse(response, content_type='application/json')


def course_details(request, course):
    course_status = []
    today = datetime.datetime.now().date()
    active_course = Course.objects.filter(name=course)
    for student in User.objects.filter(student_courses=active_course[0]):
        course_status.append({
            'student': student.username,
            'logged_in': CheckIn.objects.filter(student=student, course=active_course[0], date=today)
        })
    data = {'current_status': course_status}

    return render_to_response('includes/class_details.html', data)