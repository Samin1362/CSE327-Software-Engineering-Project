from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from Exam_System.models import Student, ComputerScience
import pyaudio, wave, time
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from pydub import AudioSegment
from thefuzz import fuzz, process
from .serializers import StudentSerializer, ComputerScienceSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


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
            return redirect('facultyGrades')

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
                student_id=4,
                student_email=user.email,
                student_marks=0
            )

            new_student.save()

            messages.success(request, 'Student Added')

            return  render(request, 'Course/Faculty/addStudent.html', {'students': students})
        
        except Exception as e:
            print(e)
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

def facultyAssignments(request):

    user = ComputerScience.objects.get(id = 1)
    print(user.student_name)
    mcq_question = user.mcq_question
    option1 = user.option_1
    option2 = user.option_2
    option3 = user.option_3
    option4 = user.option_4
    mcq_answer = user.mcq_answer

    short_question = user.short_question
    short_question_answer = user.short_answer

    broad_question = user.broad_question
    broad_question_answer = user.broad_answer

    voice_question = user.voice_question
    voice_answer = user.voice_answer

    #For Json file



    
    if request.method == 'POST':

        user.mcq_question = []
        user.option_1 = []
        user.option_2 = []
        user.option_3 = []
        user.option_4 = []
        user.mcq_answer = []

        user.short_question = []
        user.short_answer = []

        user.broad_question = []
        user.broad_answer = []

        user.voice_question = []
        user.voice_answer = []

        user.save()

        count_for_mcq = request.POST.get('hidden_mcq_question_count')
        count_for_short = request.POST.get('hidden_short_question_count')
        count_for_broad = request.POST.get('hidden_broad_question_count')
        count_for_voice = request.POST.get('hidden_voice_question_count')

        #Accessing the database
        user = ComputerScience.objects.get(id=1)
        mcq_question = user.mcq_question
        option1 = user.option_1
        option2 = user.option_2
        option3 = user.option_3
        option4 = user.option_4
        mcq_answer = user.mcq_answer

        short_question = user.short_question
        short_question_answer = user.short_answer

        broad_question = user.broad_question
        broad_question_answer = user.broad_answer

        voice_question = user.voice_question
        voice_answer = user.voice_answer

        user.number_of_mcq = count_for_mcq
        user.number_of_short = count_for_short
        user.number_of_broad = count_for_broad
        user.number_of_voice = count_for_voice

        user.exam_duration = request.POST.get('Exam_Duration')

        #Creating variable for inputs
        temp = 0
        while temp<int(count_for_mcq):

            input_mcq_question = request.POST.get(f'mcq_question_{temp + 1}')
            input_option_1 = request.POST.get(f'option{temp + 1}_1')
            input_option_2 = request.POST.get(f'option{temp + 1}_2')
            input_option_3 = request.POST.get(f'option{temp + 1}_3')
            input_option_4 = request.POST.get(f'option{temp + 1}_4')
            input_answer = request.POST.get(f'mcq_answer_{temp + 1}')

            mcq_question.append(input_mcq_question)
            option1.append(input_option_1)
            option2.append(input_option_2)
            option3.append(input_option_3)
            option4.append(input_option_4)
            mcq_answer.append(input_answer)

            user.save()

            temp+=1

        temp = 0
        while temp<int(count_for_short):

            input_short_question = request.POST.get(f'short_question_{temp + 1}')
            input_short_question_answer = request.POST.get(f'short_answer_{temp + 1}')

            short_question.append(input_short_question)
            short_question_answer.append(input_short_question_answer)

            user.save()
            temp+=1

        temp = 0
        while temp<int(count_for_broad):

            input_broad_question = request.POST.get(f'broad_question_{temp + 1}')
            input_broad_question_answer = request.POST.get(f'broad_answer_{temp + 1}')

            broad_question.append(input_broad_question)
            broad_question_answer.append(input_broad_question_answer)

            user.save()
            temp+=1

        temp = 0
        while temp<int(count_for_voice):

            input_voice_question = request.POST.get(f'voice_question_{temp + 1}')
            input_voice_question_answer = request.POST.get(f'voice_answer_{temp + 1}')

            voice_question.append(input_voice_question)
            voice_answer.append(input_voice_question_answer)

            user.save()
            temp+=1


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
            url = 'studentAssignment/?output={}'.format(username_)
            return HttpResponseRedirect(url)
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

    username_ = request.GET.get('output')

    question_ = ComputerScience.objects.get(id = 1)
    mcq_questions = question_.mcq_question
    options = [question_.option_1, question_.option_2, question_.option_3, question_.option_4]
    

    context = {
        'mcq_data': zip(mcq_questions, *options),
        'short_questions': question_.short_question,
        'broad_questions': question_.broad_question,
        'voice_questions': question_.voice_question,
        'exam_duration': question_.exam_duration,
        'username': username_,
    }


    if request.method == 'POST':

        get_username = request.POST.get('username')
        tab_changed_counter_ = request.POST.get('tab_changed_counter')
        unknown_face_percentage__ = request.POST.get('unknown_face_percentage_')


        question = ComputerScience.objects.get(student_name = get_username)

        question.tab_change_counter = tab_changed_counter_
        question.unknown_face_detection_percentage = unknown_face_percentage__
        print(question_.student_name)
        print(question.student_name)
        question.save()

        mcq_questions = question.mcq_question
        options = [question.option_1, question.option_2, question.option_3, question.option_4]

        marks_for_each_mcq = 0
        marks_for_each_short = 0
        marks_for_each_broad = 0
        marks_for_each_voice = 0

        initial_marks_mcq = question_.mcq_marks
        if question_.number_of_mcq != 0:
            marks_for_each_mcq = float(initial_marks_mcq) / float(question_.number_of_mcq)

        initial_marks_short = question_.short_marks
        if question_.number_of_short != 0:
            marks_for_each_short = float(initial_marks_short) / float(question_.number_of_short)

        initial_marks_broad = question_.broad_marks
        if question_.number_of_broad != 0:
            marks_for_each_broad = float(initial_marks_broad) / float(question_.number_of_broad)
        
        initial_marks_voice = question_.voice_marks
        if question_.number_of_voice != 0:
            marks_for_each_voice = float(initial_marks_voice) / float(question_.number_of_voice)
        

        # context = {
        #     'mcq_data': zip(mcq_questions, *options),
        #     'short_questions': question_.short_question,
        #     'broad_questions': question_.broad_question,
        #     'voice_questions': question_.voice_question,
        #     'exam_duration': question_.exam_duration,
        #     'username': username_,
        # }

        #for grading
        mark_achived_mcq = 0
        mark_achived_short = 0
        mark_achived_broad = 0
        mark_achived_voice = 0

        no_of_mcq = question_.number_of_mcq
        no_of_short = question_.number_of_short
        no_of_broad = question_.number_of_broad
        no_of_voice = question_.number_of_voice

        input_mcq_answer = []
        input_short_answer = []
        input_broad_answer = []
        input_voice_answer = []

        index = 0
        while index < no_of_mcq:
            get_mcq_answer = request.POST.get(f'mcq_{index + 1}')
            input_mcq_answer.append(get_mcq_answer)
            index += 1

        index = 0
        while index < no_of_mcq:
            ratio = fuzz.ratio(question_.mcq_answer[index], input_mcq_answer[index])
            if ratio == 100:
                mark_achived_mcq += marks_for_each_mcq
            index += 1


        #For short question 

        index = 0
        while index < no_of_short:
            get_short_answer = request.POST.get(f'short_answer_{index + 1}')
            input_short_answer.append(get_short_answer)
            index += 1

        
        index = 0
        while index < no_of_short:
            ratio = fuzz.token_set_ratio(question_.short_answer[index], input_short_answer[index])
            print(ratio)
            if ratio > 90:
                mark_achived_short += marks_for_each_short
            index += 1
        

        #For broad question 

        index = 0
        while index < no_of_broad:
            get_broad_answer = request.POST.get(f'broad_answer_{index + 1}')
            input_broad_answer.append(get_broad_answer)
            index += 1

        index = 0
        while index < no_of_broad:
            ratio = fuzz.token_sort_ratio(question_.broad_answer[index], input_broad_answer[index])
            if ratio != 0:
                ratio_percantage = (marks_for_each_broad/100) * float(ratio)
                mark_achived_broad += ratio_percantage
            else:
                ratio_percantage = 0 
            index += 1
        


        #checking voice input 

        index = 0
        while index < no_of_voice:
            get_voice_answer = request.POST.get(f'voice_answer_{index + 1}')
            input_voice_answer.append(get_voice_answer)
            index += 1

        index = 0
        while index < no_of_voice:
            ratio = fuzz.token_sort_ratio(question_.voice_answer[index], input_voice_answer[index])
            if ratio != 0:
                ratio_percantage = (marks_for_each_voice/100) * float(ratio)
                mark_achived_voice += ratio_percantage
            else:
                ratio_percantage = 0
            index += 1
        
        question.mcq_marks = mark_achived_mcq
        question.short_marks = mark_achived_short
        question.broad_marks = mark_achived_broad
        question.voice_marks = mark_achived_voice

        print(mark_achived_mcq)


        #Setting marks 
        question.student_marks = mark_achived_mcq + mark_achived_short + mark_achived_broad + mark_achived_voice
        question.save()

        voice_files = request.FILES.getlist('voice_input')

        for voice_file in voice_files:
            # Process each audio file as needed
            fs = FileSystemStorage()
            get_voice_answer = fs.save(voice_file.name, voice_file)
            audio = AudioSegment.from_wav(get_voice_answer)
            audio.export("converted_audio.wav", format="wav")



        return redirect('studentCourse')

    return render(request, 'Course/Student/assignment.html', context)

def marks(request):
    username_ = request.GET.get('output')
    student = ComputerScience.objects.get(student_name = username_)
    return render(request, "Course/Student/marks.html", {'student':student})


def facultyGrades(request):

    students = ComputerScience.objects.all()  # Fetch all student records

    return render(request, 'Course/Faculty/submitGrade.html', {'students': students})
