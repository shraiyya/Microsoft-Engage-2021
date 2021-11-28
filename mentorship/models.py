from django.db import models
from django.contrib.auth.models import User

domains=[('Machine Learning','Machine Learning'),
('Artificial Intelligence','Artificial Intelligence'),
('Front End Development','Front End Development'),
('Back End Development','Back End Development'),
('IOT','IOT'),
('HCI','HCI'),
('Data Science','Data Science'),
('Resume Building','Resume Building'),
('General College Doubts','General College Doubts'),
]


class Mentor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MentorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    domain= models.CharField(max_length=50,choices=domains,default='Data Science')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.domain)



class Mentee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/MenteeProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    interests = models.CharField(max_length=100,null=False)
    assignedMentorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.interests+")"


class Appointment(models.Model):
    menteeId=models.PositiveIntegerField(null=True)
    mentorId=models.PositiveIntegerField(null=True)
    menteeName=models.CharField(max_length=40,null=True)
    mentorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)

    
class MenteeExitDetails(models.Model):
    menteeId=models.PositiveIntegerField(null=True)
    menteeName=models.CharField(max_length=40)
    assignedMentorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    interests = models.CharField(max_length=100,null=True)
    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)
