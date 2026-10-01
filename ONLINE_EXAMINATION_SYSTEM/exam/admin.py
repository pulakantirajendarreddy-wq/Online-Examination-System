from django.contrib import admin
from .models import Student, Subject, Question, Result


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone')
    search_fields = ('email', 'phone')
    list_per_page = 10


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name')
    search_fields = ('subject_name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'subject',
        'question',
        'option1',
        'option2',
        'option3',
        'option4',
        'answer',
    )
    list_filter = ('subject',)
    search_fields = ('question',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'subject',
        'score',
        'exam_date',
    )
    list_filter = ('subject', 'exam_date')
    search_fields = ('student_email', 'subject_subject_name')