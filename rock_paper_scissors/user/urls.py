from django.urls import path
from . import views

urlpatterns = {
    path('user/signup/', views.SignupUser.as_view()),
    path('user/login/', views.LoginUser.as_view()),
    path('staff/signup/', views.SignupStaffUser.as_view()),
    path('staff/login/', views.LoginStaffUser.as_view()),
}
