
from django.contrib import admin
from django.urls import path
from mentorship import views
from django.contrib.auth.views import LoginView,LogoutView


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('mentorclick', views.mentorclick_view),
    path('menteeclick', views.menteeclick_view),

    path('adminsignup', views.admin_signup_view),
    path('mentorsignup', views.mentor_signup_view,name='mentorsignup'),
    path('menteesignup', views.mentee_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='mentorship/adminlogin.html')),
    path('mentorlogin', LoginView.as_view(template_name='mentorship/mentorlogin.html')),
    path('menteelogin', LoginView.as_view(template_name='mentorship/menteelogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='mentorship/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-mentor', views.admin_mentor_view,name='admin-mentor'),
    path('admin-view-mentor', views.admin_view_mentor_view,name='admin-view-mentor'),
    path('delete-mentor-from-mentorship/<int:pk>', views.delete_mentor_from_mentorship_view,name='delete-mentor-from-mentorship'),
    path('update-mentor/<int:pk>', views.update_mentor_view,name='update-mentor'),
    path('admin-add-mentor', views.admin_add_mentor_view,name='admin-add-mentor'),
    path('admin-approve-mentor', views.admin_approve_mentor_view,name='admin-approve-mentor'),
    path('approve-mentor/<int:pk>', views.approve_mentor_view,name='approve-mentor'),
    path('reject-mentor/<int:pk>', views.reject_mentor_view,name='reject-mentor'),
    path('admin-view-mentor-specialisation',views.admin_view_mentor_specialisation_view,name='admin-view-mentor-specialisation'),


    path('admin-mentee', views.admin_mentee_view,name='admin-mentee'),
    path('admin-view-mentee', views.admin_view_mentee_view,name='admin-view-mentee'),
    path('delete-mentee-from-mentorship/<int:pk>', views.delete_mentee_from_mentorship_view,name='delete-mentee-from-mentorship'),
    path('update-mentee/<int:pk>', views.update_mentee_view,name='update-mentee'),
    path('admin-add-mentee', views.admin_add_mentee_view,name='admin-add-mentee'),
    path('admin-approve-mentee', views.admin_approve_mentee_view,name='admin-approve-mentee'),
    path('approve-mentee/<int:pk>', views.approve_mentee_view,name='approve-mentee'),
    path('reject-mentee/<int:pk>', views.reject_mentee_view,name='reject-mentee'),
    path('admin-exit-mentee', views.admin_exit_mentee_view,name='admin-exit-mentee'),
    path('exit-mentee/<int:pk>', views.exit_mentee_view,name='exit-mentee'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('mentor-dashboard', views.mentor_dashboard_view,name='mentor-dashboard'),
    path('search', views.search_view,name='search'),

    path('mentor-mentee', views.mentor_mentee_view,name='mentor-mentee'),
    path('mentor-view-mentee', views.mentor_view_mentee_view,name='mentor-view-mentee'),
    path('mentor-view-exit-mentee',views.mentor_view_exit_mentee_view,name='mentor-view-exit-mentee'),

    path('mentor-appointment', views.mentor_appointment_view,name='mentor-appointment'),
    path('mentor-view-appointment', views.mentor_view_appointment_view,name='mentor-view-appointment'),
    path('mentor-delete-appointment',views.mentor_delete_appointment_view,name='mentor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]



urlpatterns +=[

    path('mentee-dashboard', views.mentee_dashboard_view,name='mentee-dashboard'),
    path('mentee-appointment', views.mentee_appointment_view,name='mentee-appointment'),
    path('mentee-book-appointment', views.mentee_book_appointment_view,name='mentee-book-appointment'),
    path('mentee-view-appointment', views.mentee_view_appointment_view,name='mentee-view-appointment'),
    path('mentee-view-mentor', views.mentee_view_mentor_view,name='mentee-view-mentor'),
    path('searchmentor', views.search_mentor_view,name='searchmentor'),
    path('mentee-exit', views.mentee_exit_view,name='mentee-exit'),

]
