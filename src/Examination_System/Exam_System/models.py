from django.db import models
from django.contrib.postgres.fields import ArrayField

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

    mcq_question = ArrayField(models.TextField(), default=list, blank=True)
    option_1 = ArrayField(models.CharField(max_length=150, default='Enter'), default=list, blank=True)
    option_2 = ArrayField(models.CharField(max_length=150, default='Enter'), default=list, blank=True)
    option_3 = ArrayField(models.CharField(max_length=150, default='Enter'), default=list, blank=True)
    option_4 = ArrayField(models.CharField(max_length=150, default='Enter'), default=list, blank=True)
    mcq_answer = ArrayField(models.CharField(max_length=150, default='Enter'), default=list, blank=True)

    short_question = ArrayField(models.TextField(), default=list, blank=True)
    short_answer = ArrayField(models.TextField(), default=list, blank=True)

    broad_question = ArrayField(models.TextField(), default=list, blank=True)
    broad_answer = ArrayField(models.TextField(), default=list, blank=True)
    
    voice_question = ArrayField(models.TextField(), default=list, blank=True)
    voice_answer = ArrayField(models.TextField(), default=list, blank=True)

    exam_duration = models.IntegerField(default=0)

    mcq_marks = models.DecimalField(max_digits=100, decimal_places=2, default=20.00)
    short_marks = models.DecimalField(max_digits=100, decimal_places=2, default=20.00)
    broad_marks = models.DecimalField(max_digits=100, decimal_places=2, default=40.00)
    voice_marks = models.DecimalField(max_digits=100, decimal_places=2, default=20.00)

    number_of_mcq = models.IntegerField(default=0)
    number_of_short = models.IntegerField(default=0)
    number_of_broad = models.IntegerField(default=0)
    number_of_voice = models.IntegerField(default=0)

    unknown_face_detection_percentage = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    tab_change_counter = models.IntegerField(default=0)

class VoiceRecording(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='voice_recordings/')

