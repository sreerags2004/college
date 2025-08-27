from django.urls import path
from .import views

urlpatterns = [
    path('landpage',views.landpage,name='landpage'),
    path('',views.loginpage,name='loginpage'),
    path("addcourse",views.addcourse,name='addcourse'),
    # path('teachersignup',views.teachersignup,name='teachersignup')
    path('addstudent',views.addstudent,name='addstudent'),
    path('showstudents',views.showstudents,name='showstudents'),
    path('editstudent<int:sid>',views.editstudent,name='editstudent'),
    path('deletestudent<int:sid>',views.deletestudent,name='deletestudent'),
    path('createacc',views.createacc,name='createacc'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('teacherdetails',views.teacherdetails,name='teacherdetails'),
    path('deleteteacher<int:tid>',views.deleteteacher,name='deleteteacher'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('edit_teacher',views.edit_teacher,name='edit_teacher'),
    path('editteacher<int:tid>',views.editteacher,name='editteacher'),
    path('viewteacher',views.viewteacher,name='viewteacher')
]