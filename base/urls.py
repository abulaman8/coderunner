from django.urls import path
from . import views


urlpatterns = [
    path('create-assignment/', views.create_assignment),
    path('submit-solution/<int:question_id>/', views.submit_solution),
]
