from rest_framework import serializers
from .models import Student, ComputerScience, VoiceRecording

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ComputerScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputerScience
        fields = '__all__'

class VoiceRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceRecording
        fields = '__all__'
