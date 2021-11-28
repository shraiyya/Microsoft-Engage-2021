from django import forms
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from . import models


class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class MentorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class MentorForm(forms.ModelForm):
    class Meta:
        model=models.Mentor
        fields=['address','mobile','domain','status','profile_pic']


class MenteeUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class MenteeForm(forms.ModelForm):
    
    assignedMentorId=forms.ModelChoiceField(queryset=models.Mentor.objects.all().filter(status=True),empty_label="Name and Domain", to_field_name="user_id")
    class Meta:
        model=models.Mentee
        fields=['address','mobile','status','interests','profile_pic']



class AppointmentForm(forms.ModelForm):
    mentorId=forms.ModelChoiceField(queryset=models.Mentor.objects.all().filter(status=True),empty_label="Mentor Name and Domain", to_field_name="user_id")
    menteeId=forms.ModelChoiceField(queryset=models.Mentee.objects.all().filter(status=True),empty_label="Mentee Name and Interests", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class MenteeAppointmentForm(forms.ModelForm):
    mentorId=forms.ModelChoiceField(queryset=models.Mentor.objects.all().filter(status=True),empty_label="Mentor Name and Domain", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
