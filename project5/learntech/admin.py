from django.contrib import admin
from .models import User, Course, Enrolled, Email

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password", "isTeacher")
    list_editable = ("username", "email", "password", "isTeacher")

class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "courseName", "courseTeacher", "courseData", "courseVideo", "currentlyEnrolled")
    list_editable = ("courseName", "courseTeacher", "courseData", "courseVideo", "currentlyEnrolled")

class EnrolledAdmin(admin.ModelAdmin):
    list_display = ("id", "studentName", "course")
    list_display_links = ("id", "studentName", "course")

class EmailAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "sender", "subject", "body", "timestamp", "read")
    list_display_links = ("id", "user", "sender")
    list_editable = ("subject", "body", "read")


# Register your models here.
admin.register(User),
admin.register(Course),
admin.register(Enrolled),
admin.register(Email)

admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrolled, EnrolledAdmin)
admin.site.register(Email, EmailAdmin)