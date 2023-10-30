from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/',views.user_login,name = 'login'),
    path('logout/',views.UserLogout.as_view(),name = 'logout'),
    path('singup/',views.UserSingup.as_view(),name = 'singup'),
    path('verify/<pk>/',views.Verify.as_view(),name = 'verify'),
    path('check_email/',views.CheckEmail.as_view(),name = 'check_email'),

 
    path('change_password/',views.ChangePassword.as_view(),name = 'change_password'),
    path('edit_profile/',views.EditProfile.as_view(),name = 'edit_profile'),

    path('terms&conditions/',views.TermsAndConditions.as_view(),name = 'terms&conditions'),
    path('privacy&policies/',views.PrivacyPolicy.as_view(),name = 'privacy&policies'),
    path('contactus/',views.ContactUs.as_view(),name = 'contactus'),



    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = 'authentication/forget_password.html'),name='reset_password'),

    path('reset_password_done/',auth_views.PasswordResetDoneView.as_view(template_name ='authentication/password_resetdone.html'),name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name ='authentication/password_reset.html'),name='password_reset_confirm'),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name ='authentication/password_complete.html'),name='password_reset_complete'),
]
 