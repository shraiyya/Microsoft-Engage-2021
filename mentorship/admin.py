from django.contrib import admin
from .models import Mentor,Mentee,Appointment,MenteeExitDetails
# Register your models here.
class MentorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mentor, MentorAdmin)

class MenteeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mentee, MenteeAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class MenteeExitDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(MenteeExitDetails, MenteeExitDetailsAdmin)
