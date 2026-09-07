from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('mystudents/', views.student_view, name='mystudents'),
    path('addstudent/', views.add_student_view, name='addstudent'),
    path('updatestudent/<int:id>', views.update_student_view, name='updatestudent'),
    path('deletestudent/<int:id>', views.delete_student_view, name='deletestudent'),
    #employee urls
    path('myemployees/', views.employee_view, name='myemployees'),
    path('deleteemployee/<int:id>', views.delete_employee_view, name='deleteemployee'),
    path('addemployee/', views.add_employee_view, name='addemployee'),
]
