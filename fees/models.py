from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Student(models.Model):
    COURSE_NAME=[
        ('python','Python Full Stack '),
        ('wd','Web Development'),
        ('olevel','O Level'),
        ('adca','ADCA'),
        ('dca','dca'),
        ('dtp', 'DTP'),
        ('dcfa','dcfa'),
        ('ccc','ccc'),
        ('excel','excel'),
        ('tally','tally'),
        ('word','word'),
        ('typing','typing'),
    ]


    COURSE_FEES = {
        'python': 12000,
        'wd': 3000,
        'olevel': 1200,
        'adca':500,
        'dca':500,
        'dtp':500,
        'dcfa':500,
        'ccc':800,
        'excel':1000,
        'tally':1000,
        'word':1000,
        'typing':400,
    }

    student_name=models.CharField(max_length=100)
    father_name=models.CharField(max_length=100)
    dob=models.DateField(blank=False)
    email=models.EmailField(max_length=50,unique=True)
    registration_date=models.DateField(auto_now_add=True,blank=False)
    phone_number=models.CharField(max_length=10)
    Student_id=models.CharField(max_length=100,unique=True)
    fees_date=models.DateField(blank=False) 
    course_name=models.CharField(max_length=50,choices=COURSE_NAME)
    course_fees=models.CharField()
    installment_no=models.CharField(max_length=12)
    student_img=models.ImageField(upload_to='student_photo/')



    
    def save(self, *args, **kwargs):
        if not self.student_id:
            name_parts = self.student_name.strip().split()
            first_char = name_parts[0][0].upper() if len(name_parts) > 0 else 'X'
            last_char = name_parts[-1][0].upper() if len(name_parts) > 1 else 'X'
            self.student_id = f"{first_char}{last_char}{self.phone_number}"
        super(Student, self).save(*args, **kwargs)


    def save(self, *args, **kwargs):
        # Auto-set fee before saving
        if self.course_name in self.COURSE_FEES:
            self.course_fees = self.COURSE_FEES[self.course_name]
        super().save(*args, **kwargs)


    def __str__(self):
        return self.student_name
    
class Installment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='installments')
    installment_no = models.PositiveIntegerField()
    fees_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.fees_date = self.student.fees_date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.Student_id} - Installment {self.installment_no}"

# Automatically create first installment when a Student is created
