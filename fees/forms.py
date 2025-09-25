

from datetime import date
from django import forms
from fees.models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields = '__all__'
        labels={
            'student_img':'Profile Photo',
        }
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student Name' }),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"}),
             'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # ✅ Only date (no time)
            }, format='%Y-%m-%d'),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'registration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # ✅ Only date (no time)
            }, format='%Y-%m-%d'),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'Student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID', 'id': 'id_student_id','readonly': 'readonly'}),
            'fees_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # ✅ Only date (no time)
            }, format='%Y-%m-%d'),
            'course_name': forms.Select(attrs={'class': 'form-control'}),
            'course_fees': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Fees','readonly': 'readonly'}),
            'installment_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Installment No','readonly': 'readonly'}),
            'student_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Show today's date if not editing an existing instance
        if not self.instance.pk:
            self.fields['fees_date'].initial = date.today()
            self.fields['dob'].initial=date.today()
            self.fields['installment_no'].initial=1

        if self.instance and self.instance.fees_date:
            self.fields['fees_date'].initial = self.instance.fees_date.strftime('%Y-%m-%d')
        if self.instance and self.instance.dob:
            self.fields['dob'].initial = self.instance.dob.strftime('%Y-%m-%d')



