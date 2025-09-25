from django.contrib import admin

# Register your models here.
from .models import Student, Installment

# Optional: Inline view of installments within Student admin
class InstallmentInline(admin.TabularInline):  # or admin.StackedInline
    model = Installment
    extra = 0  # No extra blank forms
    readonly_fields = ('installment_no', 'fees_date')  # prevent manual changes if needed

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'Student_id', 'course_name', 'phone_number', 'registration_date')
    search_fields = ('student_name', 'Student_id', 'phone_number')
    list_filter = ('course_name', 'registration_date')
    inlines = [InstallmentInline]  # Show installments inline

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'installment_no', 'fees_date')
    list_filter = ('fees_date',)
    search_fields = ('student__student_name', 'student__Student_id')

