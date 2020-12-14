from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .models import User, Course, Enrolled, Email


def index(request):
    allCourses = Course.objects.all()
    paginator = Paginator(allCourses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "learntech/index.html", {
        "pageTitle": "Home Page",
        'page_obj': page_obj
    })


@login_required
def course(request, courseID):
    theCourse = Course.objects.get(id = courseID)
    title = theCourse.courseName
    teacher = theCourse.courseTeacher
    content = theCourse.courseData
    if (not theCourse.courseVideo == ""):
        videoLink = theCourse.courseVideo
    else:
        videoLink = ""
    
    return render(request, "learntech/course.html", {
        "title": title,
        "teacher": teacher,
        "content": content,
        "video": videoLink,
        "theCourseID": courseID
    })


@login_required
def profile(request, name):
    enrollments = Enrolled.objects.filter(studentName = request.user)
    courseObjectList = []
    theCourse = Course()
    courseList = []

    theEmail = User.objects.get(username = name).email

    for item in enrollments:
        courseObjectList.append(item.course)

    for obj in courseObjectList:
        theCourse = Course.objects.filter(id = obj.id)
        courseList += list(theCourse)

    paginator = Paginator(courseList, 10)
    current_page_number = request.GET.get('page')
    page_obj = paginator.get_page(current_page_number)

    return render(request, "learntech/profile.html", {
        "pageTitle": name,
        'page_obj': page_obj,
        "theUsersEmail": theEmail
    })

@login_required
def userInbox(request):
    return render(request, "learntech/inbox.html")

@login_required
def getUserCourse(request):
    enrollments = Enrolled.objects.filter(studentName = request.user)
    courseObjectList = []
    theCourse = Course()
    courseList = []

    for item in enrollments:
        courseObjectList.append(item.course)

    for obj in courseObjectList:
        theCourse = Course.objects.filter(id = obj.id)
        courseList += list(theCourse)

    paginator = Paginator(courseList, 10)
    totalPages = paginator.num_pages
    current_page_number = request.GET.get('page')
    page_obj = paginator.get_page(current_page_number)

    pageNum = (page_obj.number)


    step1 = paginator.page(pageNum)
    courses_objects_list = step1.object_list
    return JsonResponse([course_object.serialize() for course_object in courses_objects_list], safe=False)


@login_required
def getMadeCourse(request):
    madeCourse = Course.objects.filter(courseTeacher = request.user.username)

    return JsonResponse([post_object.serialize() for post_object in madeCourse], safe=False)


@login_required
def getAllCourse(request):
    allCourses = Course.objects.all()
    paginator = Paginator(allCourses, 10)
    totalPages = paginator.num_pages
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    pageNum = (page_obj.number)


    if (pageNum != 1):        
        numOfObjectsMax = pageNum * 10
        numOfObjectsLow = numOfObjectsMax - 10        
        step1 = paginator.page(pageNum)
        coursesObj = step1.object_list
        return JsonResponse([courseObj.serialize() for courseObj in coursesObj], safe=False)        
    else:
        step1 = paginator.page(pageNum)
        course_objects_list = step1.object_list
        return JsonResponse([courseObj.serialize() for courseObj in course_objects_list], safe=False)


@login_required
@csrf_exempt
def getCourseID(request, courseID):
    course_objects = Course.objects.filter(id = courseID)

    return JsonResponse([course_object.serialize() for course_object in course_objects], safe=False)


@csrf_exempt
@login_required
def enroll(request, courseID):
    if (request.method != "POST"):
        return JsonResponse({"error": "POST request required."}, status=400)

    theCourse = Course.objects.get(id = courseID)
    enrollCourse = Enrolled()
    currentUserObject = User.objects.get(username = request.user.username)

    if (not Enrolled.objects.filter(studentName = currentUserObject, course = theCourse).exists()):
        enrollCourse.studentName = currentUserObject
        enrollCourse.course = theCourse
        enrollCourse.save()
        theCourse.currentlyEnrolled += 1
        theCourse.save()
    else:
        return JsonResponse({"messge": "You are already enrolled on this course"}, status=400)

    return JsonResponse({"messge": "You have successfully enrolled"}, status=201)


@csrf_exempt
@login_required
def unenroll(request, courseID):
    theCourse = Course.objects.get(id = courseID)
    enrollCourse = Enrolled()
    currentUserObject = User.objects.get(username = request.user.username)

    if (request.method != "POST"):
        return JsonResponse({"error": "POST request required."}, status=400)

    if (Enrolled.objects.filter(studentName = currentUserObject, course = theCourse).exists()):
        Enrolled.objects.filter(studentName = currentUserObject, course = theCourse).delete()
        theCourse.currentlyEnrolled -= 1
        theCourse.save()
    else:
        return JsonResponse({"messge": "You are not enrolled on this course."}, status=400)

    return JsonResponse({"messge": "You have successfully unenrolled from this course."}, status=201)


@csrf_exempt
@login_required
def create(request):
    if (request.method == "POST"):
        newCourse = Course()

        courseName = request.POST["courseName"]
        courseTeacher = request.POST["courseTeacher"]
        courseData = request.POST["courseData"]
        currentlyEnrolled = 0
        if (request.POST["courseVideo"] != ""):
            courseVideo = request.POST["courseVideo"]
            newCourse.courseVideo = courseVideo
        
        newCourse.courseName = courseName
        newCourse.courseTeacher = courseTeacher
        newCourse.courseData = courseData
        newCourse.currentlyEnrolled = currentlyEnrolled
        newCourse.save()

        return render(request, "learntech/create.html", {
            "msg": "Course Uploaded"
        })

    return render(request, "learntech/create.html")


@login_required
@csrf_exempt
def edit(request, theID):
    course_objects = Course.objects.filter(id = theID)
    
    return JsonResponse([course_object.serialize() for course_object in course_objects], safe=False)


@login_required
@csrf_exempt
def editChange(request, theID):
    updatePost = Course.objects.get(id = theID)

    if request.method == "PUT":
        data = json.loads(request.body)
        updatePost.courseData = data["courseData"]
        updatePost.save()
        return JsonResponse({"messge": "You have successfully edited this course."}, status=201)


@csrf_exempt
@login_required
def compose(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    print(data)
    emails = [email.strip() for email in data.get("recipients").split(",")]
    if emails == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with email {email} does not exist."
            }, status=400)

    # Get contents of email
    subject = data.get("subject", "")
    body = data.get("body", "")

    # Create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        email = Email(
            user=user,
            sender=request.user,
            subject=subject,
            body=body,
            read=user == request.user
        )
        email.save()
        for recipient in recipients:
            email.recipients.add(recipient)
        email.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)


@login_required
def mailbox(request, mailbox):
    # Filter emails returned based on mailbox
    if mailbox == "inbox":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            user=request.user, sender=request.user
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    emails = emails.all()
    return JsonResponse([email.serialize() for email in emails], safe=False)


@csrf_exempt
@login_required
def email(request, email_id):
    # Query for requested email
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Email must be via GET
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "learntech/login.html", {
                "message": "Invalid username and/or password.",
                "pageTitle": "Login"
            })
    else:
        return render(request, "learntech/login.html", {
            "pageTitle": "Home Page"
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        isTeacher = request.POST["isTeach"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "learntech/register.html", {
                "message": "Passwords must match.",
                "pageTitle": "Register"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.isTeacher = isTeacher
            user.save()
        except IntegrityError:
            return render(request, "learntech/register.html", {
                "message": "Username already taken.",
                "pageTitle": "Register"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "learntech/register.html", {
            "pageTitle": "Register"
        })