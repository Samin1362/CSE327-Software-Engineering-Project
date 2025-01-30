"""
URL configuration for Examination_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

#For Exam System
from Exam_System.views import login, signup, homeFaculty, homeStudent, facultyCourse, addStudent, facultyAnnouncements, facultyAssignments, studentCourse, studentAnnouncements, viewStudent, studentAssignment, marks, facultyGrades

urlpatterns = [
    path('admin/', admin.site.urls),

    #For Exam System
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('login/homeStudent/', homeStudent, name='homeStudent'),
    path('homeFaculty/', homeFaculty, name='homeFaculty'),
    path('facultyCourse/', facultyCourse, name='facultyCourse'), 
    path('addStudent/', addStudent, name='addStudent'),    
    path('announcements/', facultyAnnouncements, name='announcements'),    
    path('facultyAssignments/', facultyAssignments, name='facultyAssignments'),   
    path('login/homeStudent/studentCourse/', studentCourse, name='studentCourse'),   
    path('studentAnnouncements/', studentAnnouncements, name='studentAnnouncements'),   
    path('viewStudent/', viewStudent, name='viewStudent'),  
    path('login/homeStudent/studentCourse/studentAssignment/', studentAssignment, name='studentAssignment'), 
    path('login/homeStudent/studentCourse/marks/', marks, name='marks'), 
    path('test/', facultyGrades, name='facultyGrades'),  

]


