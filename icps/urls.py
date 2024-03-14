from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('upload/file/', views.upload_file, name="upload_file"),
    path('report/options', views.options, name='options'),
    path('employees/report/<str:ready>', views.employees_report, name="report"),
    path('report_summary/<start_date>/<end_date>/<title>', views.employee_report_summary, name="report_summary"),
    path('employees/report/icps/<str:ready>', views.icps_employees_report, name="icps_report"),
    path('report_summary/icps/<start_date>/<end_date>/<title>', views.icps_employee_report_summary,
         name="icps_report_summary"),
    path('employees/avg_report/icps/<str:ready>', views.icps_employees_avg_report, name="icps_avg_report"),
    path('avg_report_breakdown/icps/<start_date>/<end_date>/<title>', views.icps_employee_average_breakdown,
         name="icps_avg_breakdown"),
    path('user_attendance_breakdown/icps/<pk>/<title>/<start_date>/<end_date>', views.user_attendance_breakdown,
         name="user_attendance_breakdown"),

    path('employees/icps', views.icps_employees, name="icps_employees"),
    path('employees/head_office', views.octagon_employees, name="octagon_employees"),
    path('delete_icps_employee/<str:pk>', views.delete_icps_employee, name='delete_icps_employee'),
    path('delete_octagon_employee/<str:pk>', views.delete_octagon_employee, name='delete_octagon_employee'),

    path('account/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.
         as_view(template_name='users/password_reset/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.
         as_view(template_name='users/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.
         as_view(template_name='users/password_reset/password_reset_complete.html'), name='password_reset_complete'),
    path('about/', views.about, name='about'),

]

