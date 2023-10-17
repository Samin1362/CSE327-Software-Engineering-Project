from django.contrib import admin

# Register your models here.
from .models import Student, ComputerScience
admin.site.register(Student)
admin.site.register(ComputerScience)