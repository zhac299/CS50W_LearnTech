from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("create", views.create, name="create"),
    path("course/<int:courseID>", views.course, name="course"),
    path("inbox", views.userInbox, name="userInbox"),

    #JS APIs
    path("getCourse", views.getAllCourse, name="getAllCourse"),
    path("joinCourse/<int:courseID>", views.enroll, name="enroll"),
    path("leaveCourse/<int:courseID>", views.unenroll, name="unenroll"),
    path("getID/<int:courseID>", views.getCourseID, name="getCourseID"),
    path("getEnrolledCourse", views.getUserCourse, name="getUserCourse"),
    path("getTaughtCourse", views.getMadeCourse, name="getMadeCourse"),
    path("editPost/<int:theID>", views.edit, name="edit"),
    path("editUpdate/<int:theID>", views.editChange, name="editChange"),

    #inbox JS APIs
    path("emails", views.compose, name="compose"),
    path("emails/<int:email_id>", views.email, name="email"),
    path("emails/<str:mailbox>", views.mailbox, name="mailbox"),
]