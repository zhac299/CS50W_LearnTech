from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    isTeacher = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "isTeacher": self.isTeacher
        }

class Course(models.Model):
    courseName = models.TextField()
    courseTeacher = models.CharField(max_length=256)
    courseData = models.TextField()
    courseVideo = models.TextField(blank=True)
    currentlyEnrolled = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "courseName": self.courseName,
            "courseTeacher": self.courseTeacher,
            "courseData": self.courseData,
            "courseVideo": self.courseVideo,
            "currentlyEnrolled": self.currentlyEnrolled
        }

class Enrolled(models.Model):
    studentName = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def serialize(self):
        return {
            "id": self.id,
            "studentName": self.studentName,
            "course": self.course
        }

class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emails")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="emails_sent")
    recipients = models.ManyToManyField(User, related_name="emails_received")
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "read": self.read,
        }