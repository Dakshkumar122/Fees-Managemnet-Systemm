from datetime import timedelta
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from fees.forms import StudentForm
from .models import Installment, Student
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def fees(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')  # Hidden input name="student_id"

        if student_id:  
            student = get_object_or_404(Student, Student_id=student_id)
            form = StudentForm(request.POST, request.FILES, instance=student)

            # Count installments
            total_installments = Installment.objects.filter(student=student).count()
            if total_installments >= 12:
                
                messages.error(request, f"{student.student_name} has already completed all 12 installments.")
                return redirect('fees')

            # Get first installment date
            first_installment = Installment.objects.filter(student=student).order_by('fees_date').first()
            if first_installment:
                # Calculate next installment due date
                next_due_date = first_installment.fees_date + timedelta(days=30 * total_installments)
                if now().date() < next_due_date:
                    formatted_date = next_due_date.strftime("%d-%m-%Y")
                    messages.error(request, f"Next installment for {student.student_name} is due on {formatted_date}, cannot pay in advance.")
                    return redirect('fees')

        else:
            form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            student = form.save()

            installment_no = form.cleaned_data.get('installment_no')
            fees_date = form.cleaned_data.get('fees_date')

            # Count installments again (for new student case or after save)
            total_installments = Installment.objects.filter(student=student).count()
            if total_installments >= 12:
                messages.error(request, f"{student.student_name} has already completed all 12 installments.")
                return redirect('fees')

            # Get first installment date
            first_installment = Installment.objects.filter(student=student).order_by('fees_date').first()
            if first_installment:
                next_due_date = first_installment.fees_date + timedelta(days=30 * total_installments)
                if now().date() < next_due_date:
                    messages.error(request, f"Next installment for {student.student_name} is due on {next_due_date}, cannot pay in advance.")
                    return redirect('fees')

            if installment_no and fees_date:
                Installment.objects.create(
                    student=student,
                    installment_no=installment_no,
                    fees_date=fees_date
                )
                messages.success(request, "Fees collected successfully") 
            return redirect('fees')

    else:
        form = StudentForm()

    return render(request, 'index.html', {'form': form})

def search_student_ids(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        students = Student.objects.filter(Student_id__istartswith=query)[:10]
        results = [{'id': s.id, 'student_id': s.Student_id} for s in students]

    # Optionally return exact match info — not mandatory but useful for frontend
    exact_match = any(s['student_id'].lower() == query.lower() for s in results)

    return JsonResponse({
        'results': results,
        'exact_match': exact_match
    })

# Yeh function kaam karta hai jab tu ek student select karta hai (dropdown se) —
# toh uske poore details form me auto-fill ho jaate hain.
def get_student_details(request, student_id):
    try:
        student = get_object_or_404(Student, pk=student_id)
        # Get last installment number
        data = {
            'student_name': student.student_name,
            'father_name': student.father_name,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'email': student.email,
            'phone_number': student.phone_number,
            'Student_id': student.Student_id,
            'fees_date': student.fees_date.strftime('%Y-%m-%d'),
            'course_name': student.course_name,
            'course_fees': student.course_fees,
            'installment_no': int(student.installment_no)+1,
        }
        # Yeh line ye data dictionary ko JSON format me convert karke frontend (JavaScript) ko bhej rhi hai.
        return JsonResponse(data)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    




# Defaulter views ===========


def defaulter(request):
    search_query = request.GET.get('q', '').strip()
    today = timezone.now().date()
    defaulters = []
    students = Student.objects.all()

    if search_query:
        students = students.filter(Student_id__icontains=search_query)
    else:
        unpaid_only = []
        for student in students:
            installments = student.installments.order_by('fees_date')
            if not installments.exists():
                continue

            first_date = installments.first().fees_date
            months_passed = (today.year - first_date.year) * 12 + (today.month - first_date.month) + 1
            expected_installments = months_passed
            paid_installments = installments.count()
            pending = expected_installments - paid_installments

            if pending > 0:
                unpaid_only.append((student, pending))  # store with pending count

        # Sort unpaid students by max pending installments (descending)
        unpaid_only.sort(key=lambda x: x[1], reverse=True)
        students = [stu for stu, _ in unpaid_only]

    for student in students:
        installments = student.installments.order_by('fees_date')
        if not installments.exists():
            continue

        first_date = installments.first().fees_date
        months_passed = (today.year - first_date.year) * 12 + (today.month - first_date.month) + 1
        expected_installments = months_passed
        paid_installments = installments.count()
        pending = expected_installments - paid_installments

        if pending <= 0:
            color = "lightgreen" if search_query else None
        elif pending >= 5:
            color = "red"
        elif pending >= 3:
            color = "orange"
        else:
            color = "yellow"

        if color:  # skip fully paid on default load
            defaulters.append({'student': student, 'pending': pending, 'color': color})

    return render(request, 'defaulter.html', {
        'defaulters': defaulters,
        'search_query': search_query
    })


def search_student_default_ids(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        students = Student.objects.filter(Student_id__icontains=query)[:10]
        results = [{'Student_id': s.Student_id, 'name': s.student_name} for s in students]
    return JsonResponse(results, safe=False)




def collect_fees(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # Redirect to fees page with student_id as a query parameter
    return redirect(f'/fees/?q={student.Student_id}')



DELETE_PASSWORD = "admin123"  # Change this to a secure password

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    installments = student.installments.all().order_by('installment_no')

    # Find the installment with the maximum installment_no
    max_installment = installments.order_by('-installment_no').first()

    return render(request, 'details.html', {
        'student': student,
        'installments': installments,
        'max_installment': max_installment
    })


@csrf_exempt
def delete_installment(request):
    if request.method == "POST":
        inst_id = request.POST.get("id")
        password = request.POST.get("password")

        if password != DELETE_PASSWORD:
            return JsonResponse({"status": "error", "message": "Incorrect password"})

        installment = get_object_or_404(Installment, id=inst_id)
        installment.delete()

        return JsonResponse({"status": "success", "message": "Installment deleted"})

