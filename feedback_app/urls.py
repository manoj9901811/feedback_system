from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/add-faculty/', views.add_faculty, name='add_faculty'),
    path('dashboard/add-student/', views.add_student, name='add_student'),
    path('dashboard/add-subject/', views.add_subject, name='add_subject'),
    path('dashboard/assign-subject/', views.assign_subject, name='assign_subject'),
    path('dashboard/assign-section/', views.assign_section, name='assign_section'),
    path('dashboard/map-student-faculty/', views.map_student_faculty, name='map_student_faculty'),
    path('dashboard/feedback-report/', views.feedback_report, name='feedback_report'),
    path('logout/', views.logout_view, name='logout'),
    path('download-students-excel/', views.download_students_excel, name='download_students_excel'),
    path('dashboard/download-mappings-excel/', views.download_mappings_excel, name='download_mappings_excel'),
    path('dashboard/download-mappings-pdf/', views.download_mappings_pdf, name='download_mappings_pdf'),
    path('facility-feedback/', views.facility_feedback, name='facility_feedback'),
    path('course-end-feedback/', views.course_end_feedback, name='course_end_feedback'),
    path("dashboard/clear-mappings/", views.clear_mappings, name="clear_mappings"),
    path("view-faculties/", views.view_faculties, name="view_faculties"),
    path("delete-faculty/<int:faculty_id>/", views.delete_faculty, name="delete_faculty"),




]

