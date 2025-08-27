from django.shortcuts import render,redirect
from .models import Student,Course,Teacher
from django.contrib import messages,auth
from django.contrib.auth.models import  User
from django.contrib.auth import login
import os
from django.contrib.auth.decorators import login_required
@login_required(login_url='loginpage')
def teacherhome(request):
    return render(request,'teacherhome.html')
@login_required(login_url='loginpage')
def landpage(request):
    return render(request,'landingpage.html')
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pwd']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_authenticated:  # Check if the user is authenticated
                if user.is_staff:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    return redirect('landpage')
                else:
                    login(request, user)
                    request.session['user'] = user.username  # Set user session variable
                    messages.info(request, f'Welcome {user}')
                    return redirect('teacherhome')  # Redirect to techhome after login
            
        else:
            messages.info(request, 'Invalid Username or Password')
            return render(request, 'teachersignup.html',{})  
    return render(request, 'teachersignup.html')


@login_required(login_url='loginpage')
def addcourse(request):
    if request.method == 'POST':
        coursename = request.POST.get('coursename')
        fees = request.POST.get('fees')
        cource = Course(coursename=coursename,fees=fees)
        cource.save()
        messages.success(request, 'Course Added successfully!')
        return redirect('addcourse')
    return render(request,'addcourse.html')
@login_required(login_url='loginpage')
def showstudents(request):
    students = Student.objects.all()
    return render(request,'showstudents.html',{'students':students})
@login_required(login_url='loginpage')
def addstudent(request):
    course = Course.objects.all()
    if request.method== 'POST':
        studentname=request.POST.get('studentname')
        course_id=request.POST.get('course')
        course = Course.objects.get(id =course_id)
        address=request.POST.get('address')
        age=request.POST.get('age')
        joiningdate=request.POST.get('joiningdate')
        student = Student(studentname= studentname, age = age, course = course, address = address, joiningdate= joiningdate)
        student.save()
        messages.success(request,f'Student : {studentname} Added succesfully')
        return redirect('showstudents')
    else:
        return render(request,'addstudent.html',{'course':course})
    
@login_required(login_url='loginpage')
def editstudent(request,sid):
    student = Student.objects.get(id=sid)
    courses = Course.objects.all()
    if request.method == 'POST':
        student.studentname = request.POST.get('studentname')
        student.age = request.POST.get('age')
        student.address = request.POST.get('address')
        course_id = request.POST.get('course')
        student.course = Course.objects.get(id=course_id)
        student.joiningdate = request.POST.get('joiningdate')
        student.save()
        messages.success(request,'Student Editted')
        return redirect('showstudents')
    else:
        return render(request,'editstudent.html',{'student':student, 'courses':courses})
@login_required(login_url='loginpage')
def deletestudent(request,sid):
    student = Student.objects.get(id=sid)
    sname = student.studentname
    student.delete()
    messages.success(request,f'Student : {sname} Deleted succesfully')
    return redirect('showstudents')
def createacc(request):
    courses = Course.objects.all()
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        mailid = request.POST.get('mailid')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        address = request.POST.get('address')
        age = request.POST.get('age')
        phno = request.POST.get('phno')
        pfp = request.FILES.get('pfp')
        course = request.POST.get('course')
        crs = Course.objects.get(id = course)
        if cpwd == pwd:
            if User.objects.filter(username = username).exists():
                messages.info(request,'This Username Already Exist')
                return redirect('createacc')
            elif User.objects.filter(email = mailid):
                messages.info(request,'User with this Email Already Exists')
                return redirect('createacc')
            else:
                user = User.objects.create_user(first_name = fname, last_name = lname , email = mailid, password= pwd, username = username)
                user.save()
                u_name = User.objects.get(id = user.id)
                teacher = Teacher(user = u_name , age = age , address = address, phone = phno , image = pfp , course = crs)
                teacher.save()
                return redirect('loginpage')
    else:
        return render(request,'createacc.html',{'courses':courses})
def logoutuser(request):
    auth.logout(request)
    return redirect('loginpage')
@login_required(login_url='loginpage')
def teacherdetails(request):
    teachers = Teacher.objects.all()
    return render(request,'teacherdetails.html',{'teachers':teachers})
@login_required(login_url='loginpage')
def deleteteacher(request,tid):
    teacher = Teacher.objects.get(id=tid)
    usert = User.objects.get(id=teacher.user.id)
    teacher.delete()
    usert.delete()
    return redirect('teacherdetails')
@login_required(login_url='loginpage')
def edit_teacher(request):
    courses = Course.objects.all()
    teacher = Teacher.objects.get(user = request.user)
    return render(request, "cardedit.html", {'teacher':teacher,'courses':courses})
@login_required(login_url='loginpage')
def viewteacher(request):
        tchr=Teacher.objects.get(user=request.user)
        return render(request,'viewteacher.html',{'teacher':tchr})
    
@login_required(login_url='loginpage')
def editteacher(request,tid):
    if request.method == 'POST':
        teacher = Teacher.objects.get(id=tid)
        user = User.objects.get(id=teacher.user.id)
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        mailid =  request.POST.get('mailid')
        u_name= request.POST.get('username')
        if User.objects.filter(username = u_name).exclude(id=user.id).exists():
            messages.info(request,'Username Already Exists')
            return redirect('edit_teacher')
        else:
            user.username = u_name
        if User.objects.filter(email = mailid).exclude(id=user.id).exists():
            messages.info(request,'User with this Email Already Exists')
            return redirect('edit_teacher')
        else:
            user.email = mailid
        teacher.age = request.POST.get('age')
        teacher.address = request.POST.get('address')
        teacher.phone = request.POST.get('phno')
        newimage = request.FILES.get('pfp')
        if newimage:
            os.remove(teacher.image.path)
            teacher.image = newimage
        course = Course.objects.get(id = request.POST.get('course'))
        teacher.course = course
        user.save()
        teacher.save()
        messages.success(request,'teacher details edited succesfully')
        return redirect('viewteacher')
    