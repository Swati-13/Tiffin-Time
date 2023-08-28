import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User as CustomUser,Customer

#from student_management_app.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, \
 #   LeaveReportStudent, FeedBackStudent, NotificationStudent, StudentResult, OnlineClassRoom, SessionYearModel


def student_home(request):
   # student_obj=Students.objects.get(admin=request.user.id)
   # attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
   # attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    #attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
   # course=Courses.objects.get(id=student_obj.course_id.id)
   # subjects=Subjects.objects.filter(course_id=course).count()
   # subjects_data=Subjects.objects.filter(course_id=course)
   # session_obj=SessionYearModel.object.get(id=student_obj.session_year_id.id)
   # class_room=OnlineClassRoom.objects.filter(subject__in=subjects_data,is_active=True,session_years=session_obj)

    subject_name=[]
    data_present=[]
    data_absent=[]
  #  subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
   # for subject in subject_data:
    #    attendance=Attendance.objects.filter(subject_id=subject.id)
     #   attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
      #  attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
       # subject_name.append(subject.subject_name)
     #   data_present.append(attendance_present_count)
      #  data_absent.append(attendance_absent_count)

    return render(request,"customer_template/student_home_template.html")


def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Customer.objects.get(user_id=user)
    return render(request,"customer_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            student=Customer.objects.get(admin=customuser)
            student.address=address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))

@csrf_exempt
def student_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        student=Customer.objects.get(admin=request.user.id)
        student.fcm_token=token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

