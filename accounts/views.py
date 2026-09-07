from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from HrManagement import settings
from accounts.models import Student


# Create your views here.
@login_required
@never_cache
def dashboard_view(request):
    return render(request, 'dashboard.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('txtname')
        email = request.POST.get('txtmail')
        password = request.POST.get('pswd')
        confirm_password = request.POST.get('cpswd')

        if password != confirm_password:
            messages.error(request, "password and confirm password is not matching")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exists")
            return redirect('signup')
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email)
        user.save()
        messages.success(request, "logged in successfully")
        return redirect('login')

    return render(request, 'signup.html')


@login_required
def student_view(request):
    if request.user.is_superuser:
        my_students = Student.objects.all().values()
    else:
        my_students = Student.objects.filter(user_id=request.user.id).values()
    return render(request, 'display.html', {"student_data": my_students})


def add_student_view(request):
    if request.method == 'POST':
        student_name = request.POST.get("student_name")
        student_email = request.POST.get("student_email")
        education = request.POST.get("education")
        course = request.POST.get("course")
        total_fee = float(request.POST.get("total_fee"))
        fee_paid = float(request.POST.get("fee_paid"))

        if Student.objects.filter(email=student_email).exists():
            messages.error(request, "email already exists")
            return redirect('addstudent')
        student = Student.objects.create(user=request.user, name=student_name,
                                         email=student_email, education=education,
                                         course=course, total_fee=total_fee,
                                         paid_fee=fee_paid)
        pending_fee = total_fee - fee_paid
        subject = "Admission Confirmation"
        message = f"""
               Hello {student_name},


               You have successfully joined the course: {course}.
               Total Fee: ₹{total_fee}
               Fee Paid: ₹{fee_paid}
               Pending Fee: ₹{pending_fee}


               Please pay the remaining fee on time.


               Regards,
               Palle Institute
                       """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [student_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('mystudents')
    return render(request, 'addstudent.html', {"action": "Add"})


from django.http import HttpResponse


def delete_student_view(request, id):
    student = get_object_or_404(Student, id=id, user=request.user)
    student.delete()
    return redirect('mystudents')


def update_student_view(request, id):
    student = get_object_or_404(Student, id=id, user=request.user)
    if request.method == 'POST':
        student.name = request.POST.get("student_name")
        student.email = request.POST.get("student_email")
        student.education = request.POST.get("education")
        student.course = request.POST.get("course")
        student.total_fee = float(request.POST.get("total_fee"))
        student.paid_fee = float(request.POST.get("fee_paid"))
        student.save()
        return redirect('mystudents')

    return render(request, 'addstudent.html', {"action": "update", "student": student})


def employee_view(request):
    employees = User.objects.all().values()
    return render(request, 'employee_display.html', {"employee_data": employees})


def delete_employee_view(request, id):
    employee = get_object_or_404(User, id=id)
    employee.delete()
    return redirect('myemployees')


def add_employee_view(request):
    if request.method == 'POST':
        employee_name = request.POST.get("username")
        employee_email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        role = request.POST.get("role")
        if password != cpassword:
            messages.error(request, "password and confirm password is not matching")
            return redirect('addemployee')

        if User.objects.filter(email=employee_email).exists():
            messages.error(request, "email already exists")
            return redirect('addemployee')
        if role == 'admin':
            employee = User.objects.create_superuser(username=employee_name,
                                                    email=employee_email,
                                                    password=password)
        else:
            employee = User.objects.create_user(username=employee_name,
                                                 email=employee_email,
                                                 password=password)
            employee.is_active=True
            employee.is_staff=False
            employee.save()
        return redirect('myemployees')
    return render(request, "add_employee.html", {"action": "Add"})
