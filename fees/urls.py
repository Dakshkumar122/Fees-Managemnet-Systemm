from django.urls import  path

from . import views

urlpatterns = [
    path('',views.fees,name="fees"),
    path('search-student-ids/', views.search_student_ids, name='search_student_ids'),
    path('get-student-details/<str:student_id>/', views.get_student_details, name='get_student_details'),
    path('fees-defaulter-list/', views.defaulter, name="defaulter"),
    path('search-student-default-ids/', views.search_student_default_ids, name='search_student_default_ids'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),
    path('collect-fees/<int:pk>/', views.collect_fees, name='collect_fees'),
    path('delete-installment/', views.delete_installment, name='delete_installment'),
]
