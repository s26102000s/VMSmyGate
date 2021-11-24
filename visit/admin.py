from django.contrib import admin
from .models import Student, Applicant
# Register your models here.
# from django.contrib.auth.admin import UserAdmin

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "date", "from_time", "to_time"]

admin.site.register(Applicant)

    