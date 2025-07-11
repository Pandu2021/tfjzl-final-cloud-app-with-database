# onlinecourse/admin.py

from django.contrib import admin
# Impor Enrollment bersama dengan model lainnya dari models.py
from .models import Course, Lesson, Instructor, Learner, Enrollment, Question, Choice, Submission

# Add this to onlinecourse/admin.py
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4 # Number of empty forms to display

class QuestionInline(admin.StackedInline): # Or admin.TabularInline
    model = Question
    extra = 1
    show_change_link = True # Allow clicking to edit question directly

# Modify CourseAdmin in onlinecourse/admin.py
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date', 'instructor')
    list_filter = ('pub_date', 'instructor')
    search_fields = ['name', 'description']
    inlines = [QuestionInline] # Add this line to include questions within course admin

# Add this to onlinecourse/admin.py
admin.site.register(Course, CourseAdmin) # Register Course with CourseAdmin
admin.site.register(Enrollment) # Sekarang Enrollment sudah diimpor dan bisa didaftarkan
admin.site.register(Question) # Register Question
admin.site.register(Choice) # Register Choice
admin.site.register(Submission) # Register Submission