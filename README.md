

# Microsoft-Engage-2021

# MentorHub
Made by Shreya Pawaskar
---
## Screenshots

### Homepage of the Web App
![homepage snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/home_page.png)
### Admin Dashboard
![dashboard snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/admin_dashboard.png)
### Mentor Dashboard
![dashboard snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/mentor_dashboard.png)
### Mentee Dashboard
![dashboard snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/mentee_dashboard.png)
### Mentee Completion Report
![Report snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/mentee_completion_report.png)
### Mentor list from Admin
![mentor snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/mentor_list.png)
### Mentee list from Admin
![mentor snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/mentee_list.png)
### Mentee list from Admin
![mentor snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/mentee_list.png)
### Meeting List of the Mentee
![mentor snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/mentee_list_of_meetings.png)
### Admin Approval Page for a new mentor registration
![mentor snap](https://github.com/shraiyya/Microsoft-Engage-2021/blob/main/static/images/approvals_for_mentor_registration.png)
---

## Technologies Used:
- Backend - Python,Django
- Frontend - HTML,CSS,Bootstrap
- Database - Sqlite3


## Functions
### Admin
- Signup for their account. Then Login (No approval Required).
- Can register/view/approve/reject/delete mentor (approve those mentors who applied in MentorHub).
- Can admit/view/approve/reject/remove mentee (remove mentee when treatment is done).
- Can Generate/Download Mentee Report pdf 
- Can view/book/approve meetings (approve those meetings which are requested by the mentee).

### Mentor
- Apply for a job in a MentorHub. Then Login (Approval required by MentorHub Admin, Then the only mentor can log in).
- Can only view their mentee details (interests, name, mobile ) assigned to that mentor by Admin.
- Can view their mentees, who were removed by the Admin in the form of a list.
- Can view their Meetings which are booked by Admin.
- Can delete their Meeting, when the mentor attended their meeting.

### Mentee
- Create an account for joining the MentorHub. Then Login (Approval required by MentorHub Admin, Then the only mentee can log in).
- Can view assigned mentor's details like (domain, mobile, address).
- Can view their booked meeting status (pending/confirmed by Admin).
- Can book meetings. (approval required by Admin)
- Can view/download Report pdf (Only when that mentee is removed by Admin).

---

## Do you want to try my project locally? Try these steps!
- Install Python on your PC
- Download this Project as a Zip Folder and Extract it
- Make sure you download all the dependencies. cd to the directory where requirement.txt is located
```
pip install -r requirement.txt
```
- Then run the following Commands :
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```
- Now enter the following URL in Your Browser Installed On Your Pc
```
http://127.0.0.1:8000/
```

##  Do you want to get user feedback on your email? Then make changes needed for the contact us page
- Go to settings.py file
- Add your own Gmail email id and password
```
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_mail_password'
EMAIL_RECEIVING_USER = 'your_email@gmail.com'
```
- Login to Gmail through the host email id in your browser and open the following link and turn it ON
```
https://myaccount.google.com/lesssecureapps
```
## Assumptions
- Anyone can be Admin. It is assumed that a team of college students will handle the requests on this web app.
- There is no Approval required for the Admin account. 
- However, you can disable the Admin signup process and use any logic like creating a superuser.
- There must at least one mentor before taking in a mentee. 
- So first add the mentee.
- On the update page of the Admin you need to update the password.
