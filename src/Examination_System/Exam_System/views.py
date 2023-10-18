from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from Exam_System.models import Student, ComputerScience
import pyaudio, wave, time
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.
def login(request, *args, **kwargs):

    if request.method == "POST":

        action = request.POST.get('action')

        if action == 'login':

            role = request.POST.get('role')

            if role == 'Student':
                username_ = request.POST['username']
                password_ = request.POST['password']
        
                check = authenticate(username=username_, password=password_)

                if check is not None:
                    url = 'homeStudent/?output={}'.format(username_)
                    return HttpResponseRedirect(url)
                else:
                    messages.error(request, "Invalid Credentials")
                    return render(request, "Authentication/login.html", {})
            elif role == 'Faculty':
                username_ = request.POST['username']
                password_ = request.POST['password']
        
                check = authenticate(username=username_, password=password_)

                if check is not None: 
                    return redirect("homeFaculty")
                else:
                    messages.error(request, "Invalid Credentials")

        elif action == 'signup':
            return redirect('signup')


    return render(request, 'Authentication/login.html', {})

def signup(request, *args, **kwargs):
    if request.method == 'POST':
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(username=username)

        try:

            role = request.POST.get('role')

            if role == 'Student':
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                messages.success(request, "Successfully signup for Student")
                return redirect('login')
            elif role == 'Faculty':
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                messages.success(request, "Successfully signup for Faculty")
                return redirect('login')
            
        
        except:
            messages.error(request, 'Invalid User or Email, use different one')
            return render(request, "Authentication/signup.html", {})

    return render(request, 'Authentication/signup.html', {})

def homeStudent(request):

    username = request.GET.get('output')

    if request.method == 'POST':
        action = request.POST.get('View')
        username_ = request.POST.get('output')

        if action == 'View':
            print(username_)
            url = 'studentCourse/?output={}'.format(username_)
            return HttpResponseRedirect(url)
        else:
            return render(request, 'Authentication/home_Student.html', {})
        
    return render(request, 'Authentication/home_Student.html', {'username_':username})

def homeFaculty(request):

    if request.method == 'POST':
        action = request.POST.get('View')

        if action == 'View':
            return redirect('facultyCourse') 
        else:
            return render(request, 'Authentication/home_Faculty.html', {})

    return render(request, 'Authentication/home_Faculty.html', {})

def facultyCourse(request):

    if request.method == 'POST':

        action = request.POST['action']

        if action == 'Students':
            return redirect('addStudent')
        elif action == 'Announcements':
            return redirect('announcements')
        elif action == 'Assignment':
            return redirect('facultyAssignments')
        else:
            return redirect('homeFaculty')

    return render(request, 'Course/Faculty/facultyCourse.html', {})

def addStudent(request):


    students = ComputerScience.objects.all()  # Fetch all student records

    if request.method == 'POST':

        search_query = request.POST.get('search_query')

        try:
            get_object_or_404(User, email=search_query)

            user = User.objects.get(email=search_query)

            new_student = ComputerScience(
                student_name=user.username,
                student_id=3,
                student_email=user.email,
                student_marks=0
            )

            new_student.save()

            messages.success(request, 'Student Added')

            return  render(request, 'Course/Faculty/addStudent.html', {'students': students})
        
        except:

            messages.error(request, "Need Valid Email")
            return render(request, 'Course/Faculty/addStudent.html', {'students': students})
 
    return render(request, 'Course/Faculty/addStudent.html', {'students': students})

def facultyAnnouncements(request):

    if request.method == 'POST':

        announcement_ = request.POST.get('announcement')

        computerScienceStudent = ComputerScience.objects.all()

        for index in computerScienceStudent:
            index.announcement = announcement_
            index.save()

        messages.success(request, "Announcement Posted")

        return render(request, 'Course/Faculty/announcements.html', {})

    
    return render(request, 'Course/Faculty/announcements.html', {})

#Need to add many things
def facultyAssignments(request):

    if request.method == 'POST':

        exam_duration_ = request.POST.get('exam_duration')

        mcq_question_ = request.POST.get('mcq_question')

        option_1 = request.POST.get('option1')
        option_2 = request.POST.get('option2')
        option_3 = request.POST.get('option3')
        option_4 = request.POST.get('option4')
        mcq_answer_ = request.POST.get('mcq_answer')

        short_question_ = request.POST.get('short_question')
        short_answer_ = request.POST.get('short_answer')

        broad_question_ = request.POST.get('broad_question')
        broad_answer_ = request.POST.get('broad_answer')

        voice_question_ = request.POST.get('voice_question')
        voice_answer_ = request.POST.get('voice_answer')


        computerScienceStudent = ComputerScience.objects.all()

        for index in computerScienceStudent:

            index.exam_duration = exam_duration_

            index.mcq_question = mcq_question_

            index.option_1 = option_1
            index.option_2 = option_2
            index.option_3 = option_3
            index.option_4 = option_4

            index.mcq_answer = mcq_answer_

            index.short_question = short_question_
            index.short_answer = short_answer_

            index.broad_question = broad_question_
            index.broad_answer = broad_answer_

            index.voice_question = voice_question_
            index.voice_answer = voice_answer_

            index.save()

        messages.success(request, "Question added")

        return render(request, 'Course/Faculty/assignment.html', {})
    
    return render(request, 'Course/Faculty/assignment.html', {})
    
def studentCourse(request):

    username = request.GET.get('output')


    if request.method == 'POST':

        action = request.POST['action']
        username_ = request.POST.get('output')

        if action == 'Students':
            return redirect('viewStudent')
        elif action == 'Announcements':
            return redirect('studentAnnouncements')
        elif action == 'Assignment':
            return redirect('studentAssignment')
        else:
            url = 'marks/?output={}'.format(username_)
            return HttpResponseRedirect(url)

    return render(request, 'Course/Student/studentCourse.html', {'username_':username})    

def studentAnnouncements(request):

    announcement = ComputerScience.objects.get(id=1)
    
    return render(request, 'Course/Student/announcements.html', {'object':announcement.announcement})

def viewStudent(request):

    students = ComputerScience.objects.all()  # Fetch all student records
 
    return render(request, 'Course/Student/viewStudent.html', {'students': students})

def studentAssignment(request):

    question = ComputerScience.objects.get(id=1)

    context = {
        'question':question
    }

    if request.method == 'POST':

        email_ = request.POST.get('email')
        mcq_answer_ = request.POST.get('mcq_answer')
        short_answer_ = request.POST.get('short-answer')
        broad_answer_ = request.POST.get('broad-answer')



        student = ComputerScience.objects.get(student_email=email_)

        if student is not None: 

            if student.mcq_answer == mcq_answer_:
                student.mcq_marks = 20.00
            elif student.mcq_answer != mcq_answer_:
                student.mcq_marks = 0.00
                
            if student.short_answer == short_answer_:
                student.short_marks = 20.00
            elif student.short_answer != short_answer_:
                student.short_answer = 0.00

            student.student_marks = float(student.mcq_marks) + float(student.short_marks) + float(student.broad_marks) + float(student.voice_marks)

            student.save()
            


        audio = pyaudio.PyAudio()
        start_time = time.time()
        recording_duration = 10

        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        frames = []

        while time.time() - start_time < recording_duration:  
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open("/Users/md.saminisrak/Desktop/Input_Test/myrecording.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()



        return redirect('studentCourse')

    return render(request, 'Course/Student/assignment.html', context)

def marks(request):
    username_ = request.GET.get('output')
    student = ComputerScience.objects.get(student_name = username_)
    return render(request, "Course/Student/marks.html", {'student':student})





