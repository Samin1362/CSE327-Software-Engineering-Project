from django.db import models

# Create your models here.

class Student(models.Model):
    student_name = models.CharField(max_length=20)
    student_id = models.IntegerField(default=0)
    student_email = models.EmailField()
    student_marks = models.DecimalField(max_digits=100, decimal_places=2)

class ComputerScience(models.Model):
    student_name = models.CharField(max_length=20)
    student_id = models.IntegerField(default=0)
    student_email = models.EmailField()
    student_marks = models.DecimalField(max_digits=100, decimal_places=2)
    announcement = models.TextField(default='Add Announcement')

    mcq_question = models.TextField(default='Enter')
    option_1 = models.CharField(max_length=150, default='Enter')
    option_2 = models.CharField(max_length=150, default='Enter')
    option_3 = models.CharField(max_length=150, default='Enter')
    option_4 = models.CharField(max_length=150, default='Enter')
    mcq_answer = models.CharField(max_length=150, default='Enter')

    short_question = models.TextField(default='Enter', blank=True)
    short_answer = models.TextField(default='Enter', blank=True)

    broad_question = models.TextField(default='Enter', blank=True)
    broad_answer = models.TextField(default='Enter', blank=True)
    
    voice_question = models.TextField(default='Enter', blank=True)
    voice_answer = models.TextField(default='Enter', blank=True)

    exam_duration = models.IntegerField(default=0)

    mcq_marks = models.DecimalField(max_digits=100, decimal_places=2, default=20.00)
    short_marks = models.DecimalField(max_digits=100, decimal_places=2, default=20.00)
    broad_marks = models.DecimalField(max_digits=100, decimal_places=2, default=40.00)
    voice_marks = models.DecimalField(max_digits=100, decimal_places=2, default=20.00)

class VoiceRecording(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='voice_recordings/')

