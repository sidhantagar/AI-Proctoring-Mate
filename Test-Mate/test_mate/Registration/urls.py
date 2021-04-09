from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # SignUp
    path('',views.Register,name='registration_page'),
    # LogIn
    path('login/',views.Login,name='login_page'),
    # LogOut
    path('logout/',views.Logout,name='logout_page'),
    # NOTE : Temp URL to use later
    path('sec/',views.Secondary),

    # Reverse URL for Activating Account using unique activation link
    path('activate/<uidb64>/<token>',views.Activate,name = 'activate'),

    # Password Reset Event - URLs
    # URL1 - should take to the : enter e-mail page
    path('resetPassword/',views.PasswordResetEmailForm,name='request_password_reset'),
    # URL2 - Reverse for validating if the User exists, who asked for Password Reset
    path('resetPassword/<uidb64>/<token>',views.SetNewPassword,name='new_password'),
    # URL3 - Password Reset Form
    path('resetPassword/setPassword/',views.NewPassword,name='set_new_password'),
    # URL4 - Confirmation of password reset success
    path('resetPassword/PasswordChanged/',views.PwdChangedConfirmation,name='pwd_changed'),
]
