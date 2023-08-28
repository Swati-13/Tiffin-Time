import json
from datetime import datetime
from time import timezone
from uuid import uuid4
from datetime import date

from django.db.models.fields import DurationField
from .models import User as CustomUser,Employee, Validity_pack, FeedBackStaffs, NotificationStaffs
from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

#from .models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, \
 #   LeaveReportStaff, Staffs, FeedBackStaffs, Courses, NotificationStaffs, StudentResult, OnlineClassRoom


def staff_home(request):
    #For Fetch All Student Under Staff
    #subjects=Subjects.objects.filter(staff_id=request.user.id)
    #course_id_list=[]
    #for subject in subjects:
    #    course=Courses.objects.get(id=subject.course_id.id)
    #    course_id_list.append(course.id)

    #final_course=[]
    #removing Duplicate Course ID
    #for course_id in course_id_list:
     #   if course_id not in final_course:
      #      final_course.append(course_id)

    #students_count=Students.objects.filter(course_id__in=final_course).count()

    #Fetch All Attendance Count
    #attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #Fetch All Approve Leave
    #staff=Staffs.objects.get(admin=request.user.id)
    #leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    #ubject_count=subjects.count()

    #Fetch Attendance Data by Subject
    #subject_list=[]
    #attendance_list=[]
    #for subject in subjects:
     #   attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
      #  subject_list.append(subject.subject_name)
       # attendance_list.append(attendance_count1)

    #students_attendance=Students.objects.filter(course_id__in=final_course)
    #student_list=[]
    #student_list_attendance_present=[]
    #student_list_attendance_absent=[]
    #for student in students_attendance:
     #   attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
      #  attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
       # student_list.append(student.admin.username)
       # student_list_attendance_present.append(attendance_present_count)
       # student_list_attendance_absent.append(attendance_absent_count)


#{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent}
    return render(request,"staff_template/staff_home_template.html")

def staff_take_attendance(request):
   # subjects=Subjects.objects.filter(staff_id=request.user.id)
    #session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_take_attendance.html")

#@csrf_exempt
#def get_students(request):
 #   subject_id=request.POST.get("subject")
  #  session_year=request.POST.get("session_year")

   
    
def staff_profile(request):
    print(request.user.id)
    user1=CustomUser.objects.get(id=request.user.id)
    staff=Employee.objects.get(user=user1)
    return render(request,"staff_template/staff_profile.html",{"user":user1,"staff":staff})


def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
                customuser.save()
                messages.success(request, "Successfully Updated Profile")
                return HttpResponseRedirect(reverse("login1"))
            customuser.save()

            staff=Employee.objects.get(user=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))



def staff_account(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=Employee.objects.get(user=customuser)
    packs=Validity_pack.objects.all()
    return render(request,"staff_template/staff_account.html",{"user":customuser,"staff":staff,"packs":packs})


def staff_account_save(request):
     if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_account"))
     else:
        license=request.POST.get("license")
        Validity=request.POST.get("Validity")
        try:
            user=CustomUser.objects.get(id=request.user.id)
            user.save()
            print(user.id)
            staff=Employee.objects.get(user_id=user.id)
            staff.license=license
            print(license)
            staff.acc_id=Validity
            print(Validity)
            staff.save()
            messages.success(request, "Successfully Updated Account")
            print("yayy")
            return HttpResponseRedirect(reverse("staff_account"))
        except:
            messages.error(request, "Failed to Update Account")
            print("nayyy")
            return HttpResponseRedirect(reverse("staff_account"))

def staff_feedback(request):
    staff_id=Employee.objects.get(user_id=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Employee.objects.get(user_id=request.user.id)
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def staff_all_notification(request):
    staff=Employee.objects.get(user_id=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff)
    return render(request,"staff_template/all_notification.html",{"notifications":notifications})

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Employee.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")



def save_student_result(request):
    if request.method!='POST':
        return HttpResponseRedirect('staff_add_result')
    student_admin_id=request.POST.get('student_list')
    assignment_marks=request.POST.get('assignment_marks')
    exam_marks=request.POST.get('exam_marks')
    subject_id=request.POST.get('subject')


    #student_obj=Students.objects.get(admin=student_admin_id)
    #subject_obj=Subjects.objects.get(id=subject_id)




   

def returnHtmlWidget(request):
    return render(request,"widget.html")