from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt 
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mentorship/index.html')

@csrf_exempt 

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mentorship/adminclick.html')

@csrf_exempt 
def mentorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mentorship/mentorclick.html')

@csrf_exempt 
#for showing signup/login button for mentee
def menteeclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'mentorship/menteeclick.html')



@csrf_exempt 
def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'mentorship/adminsignup.html',{'form':form})



@csrf_exempt 
def mentor_signup_view(request):
    userForm=forms.MentorUserForm()
    mentorForm=forms.MentorForm()
    mydict={'userForm':userForm,'mentorForm':mentorForm}
    if request.method=='POST':
        userForm=forms.MentorUserForm(request.POST)
        mentorForm=forms.MentorForm(request.POST,request.FILES)
        if userForm.is_valid() and mentorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mentor=mentorForm.save(commit=False)
            mentor.user=user
            mentor=mentor.save()
            my_mentor_group = Group.objects.get_or_create(name='DOCTOR')
            my_mentor_group[0].user_set.add(user)
        return HttpResponseRedirect('mentorlogin')
    return render(request,'mentorship/mentorsignup.html',context=mydict)

@csrf_exempt 
def mentee_signup_view(request):
    userForm=forms.MenteeUserForm()
    menteeForm=forms.MenteeForm()
    mydict={'userForm':userForm,'menteeForm':menteeForm}
    if request.method=='POST':
        userForm=forms.MenteeUserForm(request.POST)
        menteeForm=forms.MenteeForm(request.POST,request.FILES)
        if userForm.is_valid() and menteeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mentee=menteeForm.save(commit=False)
            mentee.user=user
            mentee.assignedMentorId=request.POST.get('assignedMentorId')
            mentee=mentee.save()
            my_mentee_group = Group.objects.get_or_create(name='PATIENT')
            my_mentee_group[0].user_set.add(user)
        return HttpResponseRedirect('menteelogin')
    return render(request,'mentorship/menteesignup.html',context=mydict)






@csrf_exempt 
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_mentor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_mentee(user):
    return user.groups.filter(name='PATIENT').exists()



@csrf_exempt 
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_mentor(request.user):
        accountapproval=models.Mentor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('mentor-dashboard')
        else:
            return render(request,'mentorship/mentor_wait_for_approval.html')
    elif is_mentee(request.user):
        accountapproval=models.Mentee.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('mentee-dashboard')
        else:
            return render(request,'mentorship/mentee_wait_for_approval.html')








@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    mentors=models.Mentor.objects.all().order_by('-id')
    mentees=models.Mentee.objects.all().order_by('-id')
    #for three cards
    mentorcount=models.Mentor.objects.all().filter(status=True).count()
    pendingmentorcount=models.Mentor.objects.all().filter(status=False).count()

    menteecount=models.Mentee.objects.all().filter(status=True).count()
    pendingmenteecount=models.Mentee.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'mentors':mentors,
    'mentees':mentees,
    'mentorcount':mentorcount,
    'pendingmentorcount':pendingmentorcount,
    'menteecount':menteecount,
    'pendingmenteecount':pendingmenteecount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'mentorship/admin_dashboard.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_mentor_view(request):
    return render(request,'mentorship/admin_mentor.html')


@csrf_exempt 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_mentor_view(request):
    mentors=models.Mentor.objects.all().filter(status=True)
    return render(request,'mentorship/admin_view_mentor.html',{'mentors':mentors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_mentor_from_mentorship_view(request,pk):
    mentor=models.Mentor.objects.get(id=pk)
    user=models.User.objects.get(id=mentor.user_id)
    user.delete()
    mentor.delete()
    return redirect('admin-view-mentor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_mentor_view(request,pk):
    mentor=models.Mentor.objects.get(id=pk)
    user=models.User.objects.get(id=mentor.user_id)

    userForm=forms.MentorUserForm(instance=user)
    mentorForm=forms.MentorForm(request.FILES,instance=mentor)
    mydict={'userForm':userForm,'mentorForm':mentorForm}
    if request.method=='POST':
        userForm=forms.MentorUserForm(request.POST,instance=user)
        mentorForm=forms.MentorForm(request.POST,request.FILES,instance=mentor)
        if userForm.is_valid() and mentorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mentor=mentorForm.save(commit=False)
            mentor.status=True
            mentor.save()
            return redirect('admin-view-mentor')
    return render(request,'mentorship/admin_update_mentor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_mentor_view(request):
    userForm=forms.MentorUserForm()
    mentorForm=forms.MentorForm()
    mydict={'userForm':userForm,'mentorForm':mentorForm}
    if request.method=='POST':
        userForm=forms.MentorUserForm(request.POST)
        mentorForm=forms.MentorForm(request.POST, request.FILES)
        if userForm.is_valid() and mentorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            mentor=mentorForm.save(commit=False)
            mentor.user=user
            mentor.status=True
            mentor.save()

            my_mentor_group = Group.objects.get_or_create(name='DOCTOR')
            my_mentor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-mentor')
    return render(request,'mentorship/admin_add_mentor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_mentor_view(request):
    #those whose approval are needed
    mentors=models.Mentor.objects.all().filter(status=False)
    return render(request,'mentorship/admin_approve_mentor.html',{'mentors':mentors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_mentor_view(request,pk):
    mentor=models.Mentor.objects.get(id=pk)
    mentor.status=True
    mentor.save()
    return redirect(reverse('admin-approve-mentor'))

@csrf_exempt 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_mentor_view(request,pk):
    mentor=models.Mentor.objects.get(id=pk)
    user=models.User.objects.get(id=mentor.user_id)
    user.delete()
    mentor.delete()
    return redirect('admin-approve-mentor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_mentor_specialisation_view(request):
    mentors=models.Mentor.objects.all().filter(status=True)
    return render(request,'mentorship/admin_view_mentor_specialisation.html',{'mentors':mentors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_mentee_view(request):
    return render(request,'mentorship/admin_mentee.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_mentee_view(request):
    mentees=models.Mentee.objects.all().filter(status=True)
    return render(request,'mentorship/admin_view_mentee.html',{'mentees':mentees})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_mentee_from_mentorship_view(request,pk):
    mentee=models.Mentee.objects.get(id=pk)
    user=models.User.objects.get(id=mentee.user_id)
    user.delete()
    mentee.delete()
    return redirect('admin-view-mentee')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_mentee_view(request,pk):
    mentee=models.Mentee.objects.get(id=pk)
    user=models.User.objects.get(id=mentee.user_id)

    userForm=forms.MenteeUserForm(instance=user)
    menteeForm=forms.MenteeForm(request.FILES,instance=mentee)
    mydict={'userForm':userForm,'menteeForm':menteeForm}
    if request.method=='POST':
        userForm=forms.MenteeUserForm(request.POST,instance=user)
        menteeForm=forms.MenteeForm(request.POST,request.FILES,instance=mentee)
        if userForm.is_valid() and menteeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            mentee=menteeForm.save(commit=False)
            mentee.status=True
            mentee.assignedMentorId=request.POST.get('assignedMentorId')
            mentee.save()
            return redirect('admin-view-mentee')
    return render(request,'mentorship/admin_update_mentee.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_mentee_view(request):
    userForm=forms.MenteeUserForm()
    menteeForm=forms.MenteeForm()
    mydict={'userForm':userForm,'menteeForm':menteeForm}
    if request.method=='POST':
        userForm=forms.MenteeUserForm(request.POST)
        menteeForm=forms.MenteeForm(request.POST,request.FILES)
        if userForm.is_valid() and menteeForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            mentee=menteeForm.save(commit=False)
            mentee.user=user
            mentee.status=True
            mentee.assignedMentorId=request.POST.get('assignedMentorId')
            mentee.save()

            my_mentee_group = Group.objects.get_or_create(name='PATIENT')
            my_mentee_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-mentee')
    return render(request,'mentorship/admin_add_mentee.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_mentee_view(request):
    #those whose approval are needed
    mentees=models.Mentee.objects.all().filter(status=False)
    return render(request,'mentorship/admin_approve_mentee.html',{'mentees':mentees})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_mentee_view(request,pk):
    mentee=models.Mentee.objects.get(id=pk)
    mentee.status=True
    mentee.save()
    return redirect(reverse('admin-approve-mentee'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_mentee_view(request,pk):
    mentee=models.Mentee.objects.get(id=pk)
    user=models.User.objects.get(id=mentee.user_id)
    user.delete()
    mentee.delete()
    return redirect('admin-approve-mentee')




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_exit_mentee_view(request):
    mentees=models.Mentee.objects.all().filter(status=True)
    return render(request,'mentorship/admin_exit_mentee.html',{'mentees':mentees})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def exit_mentee_view(request,pk):
    mentee=models.Mentee.objects.get(id=pk)
    days=(date.today()-mentee.admitDate) #2 days, 0:00:00
    assignedMentor=models.User.objects.all().filter(id=mentee.assignedMentorId)
    d=days.days # only how many day that is 2
    menteeDict={
        'menteeId':pk,
        'name':mentee.get_name,
        'mobile':mentee.mobile,
        'address':mentee.address,
        'interests':mentee.interests,
        'admitDate':mentee.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedMentorName':assignedMentor[0].first_name,
    }
    if request.method == 'POST':
        pDD=models.MenteeExitDetails()
        pDD.menteeId=pk
        pDD.menteeName=mentee.get_name
        pDD.assignedMentorName=assignedMentor[0].first_name
        pDD.address=mentee.address
        pDD.mobile=mentee.mobile
        pDD.interests=mentee.interests
        pDD.admitDate=mentee.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.save()
        return render(request,'mentorship/mentee_final_bill.html',context=menteeDict)
    return render(request,'mentorship/mentee_generate_bill.html',context=menteeDict)


import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    exitDetails=models.MenteeExitDetails.objects.all().filter(menteeId=pk).order_by('-id')[:1]
    dict={
        'menteeName':exitDetails[0].menteeName,
        'assignedMentorName':exitDetails[0].assignedMentorName,
        'address':exitDetails[0].address,
        'mobile':exitDetails[0].mobile,
        'interests':exitDetails[0].interests,
        'admitDate':exitDetails[0].admitDate,
        'releaseDate':exitDetails[0].releaseDate,
        'daySpent':exitDetails[0].daySpent,
    }
    return render_to_pdf('mentorship/download_bill.html',dict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'mentorship/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'mentorship/admin_view_appointment.html',{'appointments':appointments})


@csrf_exempt 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.mentorId=request.POST.get('mentorId')
            appointment.menteeId=request.POST.get('menteeId')
            appointment.mentorName=models.User.objects.get(id=request.POST.get('mentorId')).first_name
            appointment.menteeName=models.User.objects.get(id=request.POST.get('menteeId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'mentorship/admin_add_appointment.html',context=mydict)


@csrf_exempt 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'mentorship/admin_approve_appointment.html',{'appointments':appointments})


@csrf_exempt 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')

@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def mentor_dashboard_view(request):
    #for three cards
    menteecount=models.Mentee.objects.all().filter(status=True,assignedMentorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,mentorId=request.user.id).count()
    menteeexitd=models.MenteeExitDetails.objects.all().distinct().filter(assignedMentorName=request.user.first_name).count()

    #for  table in mentor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,mentorId=request.user.id).order_by('-id')
    menteeid=[]
    for a in appointments:
        menteeid.append(a.menteeId)
    mentees=models.Mentee.objects.all().filter(status=True,user_id__in=menteeid).order_by('-id')
    appointments=zip(appointments,mentees)
    mydict={
    'menteecount':menteecount,
    'appointmentcount':appointmentcount,
    'menteeexitd':menteeexitd,
    'appointments':appointments,
    'mentor':models.Mentor.objects.get(user_id=request.user.id), #for profile picture of mentor in sidebar
    }
    return render(request,'mentorship/mentor_dashboard.html',context=mydict)



@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def mentor_mentee_view(request):
    mydict={
    'mentor':models.Mentor.objects.get(user_id=request.user.id), #for profile picture of mentor in sidebar
    }
    return render(request,'mentorship/mentor_mentee.html',context=mydict)





@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def mentor_view_mentee_view(request):
    mentees=models.Mentee.objects.all().filter(status=True,assignedMentorId=request.user.id)
    mentor=models.Mentor.objects.get(user_id=request.user.id) #for profile picture of mentor in sidebar
    return render(request,'mentorship/mentor_view_mentee.html',{'mentees':mentees,'mentor':mentor})


@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def search_view(request):
    mentor=models.Mentor.objects.get(user_id=request.user.id) #for profile picture of mentor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    mentees=models.Mentee.objects.all().filter(status=True,assignedMentorId=request.user.id).filter(Q(interests__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'mentorship/mentor_view_mentee.html',{'mentees':mentees,'mentor':mentor})


@csrf_exempt 
@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def mentor_view_exit_mentee_view(request):
    exitdmentees=models.MenteeExitDetails.objects.all().distinct().filter(assignedMentorName=request.user.first_name)
    mentor=models.Mentor.objects.get(user_id=request.user.id) #for profile picture of mentor in sidebar
    return render(request,'mentorship/mentor_view_exit_mentee.html',{'exitdmentees':exitdmentees,'mentor':mentor})


@csrf_exempt 
@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def mentor_appointment_view(request):
    mentor=models.Mentor.objects.get(user_id=request.user.id) #for profile picture of mentor in sidebar
    return render(request,'mentorship/mentor_appointment.html',{'mentor':mentor})


@csrf_exempt 
@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def mentor_view_appointment_view(request):
    mentor=models.Mentor.objects.get(user_id=request.user.id) #for profile picture of mentor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,mentorId=request.user.id)
    menteeid=[]
    for a in appointments:
        menteeid.append(a.menteeId)
    mentees=models.Mentee.objects.all().filter(status=True,user_id__in=menteeid)
    appointments=zip(appointments,mentees)
    return render(request,'mentorship/mentor_view_appointment.html',{'appointments':appointments,'mentor':mentor})



@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def mentor_delete_appointment_view(request):
    mentor=models.Mentor.objects.get(user_id=request.user.id) #for profile picture of mentor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,mentorId=request.user.id)
    menteeid=[]
    for a in appointments:
        menteeid.append(a.menteeId)
    mentees=models.Mentee.objects.all().filter(status=True,user_id__in=menteeid)
    appointments=zip(appointments,mentees)
    return render(request,'mentorship/mentor_delete_appointment.html',{'appointments':appointments,'mentor':mentor})



@login_required(login_url='mentorlogin')
@user_passes_test(is_mentor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    mentor=models.Mentor.objects.get(user_id=request.user.id) #for profile picture of mentor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,mentorId=request.user.id)
    menteeid=[]
    for a in appointments:
        menteeid.append(a.menteeId)
    mentees=models.Mentee.objects.all().filter(status=True,user_id__in=menteeid)
    appointments=zip(appointments,mentees)
    return render(request,'mentorship/mentor_delete_appointment.html',{'appointments':appointments,'mentor':mentor})

@login_required(login_url='menteelogin')
@user_passes_test(is_mentee)
def mentee_dashboard_view(request):
    mentee=models.Mentee.objects.get(user_id=request.user.id)
    mentor=models.Mentor.objects.get(user_id=mentee.assignedMentorId)
    mydict={
    'mentee':mentee,
    'mentorName':mentor.get_name,
    'mentorMobile':mentor.mobile,
    'mentorAddress':mentor.address,
    'interests':mentee.interests,
    'mentorDepartment':mentor.domain,
    'admitDate':mentee.admitDate,
    }
    return render(request,'mentorship/mentee_dashboard.html',context=mydict)



@login_required(login_url='menteelogin')
@user_passes_test(is_mentee)
def mentee_appointment_view(request):
    mentee=models.Mentee.objects.get(user_id=request.user.id) #for profile picture of mentee in sidebar
    return render(request,'mentorship/mentee_appointment.html',{'mentee':mentee})



@login_required(login_url='menteelogin')
@user_passes_test(is_mentee)
def mentee_book_appointment_view(request):
    appointmentForm=forms.MenteeAppointmentForm()
    mentee=models.Mentee.objects.get(user_id=request.user.id) #for profile picture of mentee in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'mentee':mentee,'message':message}
    if request.method=='POST':
        appointmentForm=forms.MenteeAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('mentorId'))
            desc=request.POST.get('description')

            mentor=models.Mentor.objects.get(user_id=request.POST.get('mentorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.mentorId=request.POST.get('mentorId')
            appointment.menteeId=request.user.id 
            appointment.mentorName=models.User.objects.get(id=request.POST.get('mentorId')).first_name
            appointment.menteeName=request.user.first_name 
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('mentee-view-appointment')
    return render(request,'mentorship/mentee_book_appointment.html',context=mydict)



def mentee_view_mentor_view(request):
    mentors=models.Mentor.objects.all().filter(status=True)
    mentee=models.Mentee.objects.get(user_id=request.user.id) #for profile picture of mentee in sidebar
    return render(request,'mentorship/mentee_view_mentor.html',{'mentee':mentee,'mentors':mentors})



def search_mentor_view(request):
    mentee=models.Mentee.objects.get(user_id=request.user.id) #for profile picture of mentee in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    mentors=models.Mentor.objects.all().filter(status=True).filter(Q(domain__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'mentorship/mentee_view_mentor.html',{'mentee':mentee,'mentors':mentors})




@login_required(login_url='menteelogin')
@user_passes_test(is_mentee)
def mentee_view_appointment_view(request):
    mentee=models.Mentee.objects.get(user_id=request.user.id) #for profile picture of mentee in sidebar
    appointments=models.Appointment.objects.all().filter(menteeId=request.user.id)
    return render(request,'mentorship/mentee_view_appointment.html',{'appointments':appointments,'mentee':mentee})



@login_required(login_url='menteelogin')
@user_passes_test(is_mentee)
def mentee_exit_view(request):
    mentee=models.Mentee.objects.get(user_id=request.user.id) #for profile picture of mentee in sidebar
    exitDetails=models.MenteeExitDetails.objects.all().filter(menteeId=mentee.id).order_by('-id')[:1]
    menteeDict=None
    if exitDetails:
        menteeDict ={
        'is_exitd':True,
        'mentee':mentee,
        'menteeId':mentee.id,
        'menteeName':mentee.get_name,
        'assignedMentorName':exitDetails[0].assignedMentorName,
        'address':mentee.address,
        'mobile':mentee.mobile,
        'interests':mentee.interests,
        'admitDate':mentee.admitDate,
        'releaseDate':exitDetails[0].releaseDate,
        'daySpent':exitDetails[0].daySpent,
        }
        print(menteeDict)
    else:
        menteeDict={
            'is_exits':False,
            'mentee':mentee,
            'menteeId':request.user.id,
        }
    return render(request,'mentorship/mentee_exit.html',context=menteeDict)



def aboutus_view(request):
    return render(request,'mentorship/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'mentorship/contactussuccess.html')
    return render(request, 'mentorship/contactus.html', {'form':sub})
