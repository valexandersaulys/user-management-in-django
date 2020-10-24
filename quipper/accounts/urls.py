from django.urls import path, include

from accounts.views import *


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/", UserDetailView.as_view(), name="user_profile"),
]

""" # include("django.contrib.auth.urls") has the following:

# this needs to be put in a table as a cheat sheet!!!

registration/login.html
django.contrib.auth.LoginView
accounts/login/ [name='login']

registration/logged_out.html
django.contrib.auth.LogoutView
accounts/logout/ [name='logout']

registration/password_change_form.html
django.contrib.auth.PasswordChangeView
accounts/password_change/ [name='password_change']

registration/password_change_done.html
django.contrib.auth.PasswordChangeDoneView
accounts/password_change/done/ [name='password_change_done']

registration/password_reset_form.html    # to enter your email as "form" object
registration/password_reset_email.html   # email text
registration/password_reset_subject.txt  # subject line for the email 
django.contrib.auth.PasswordResetView
accounts/password_reset/ [name='password_reset']

registration/password_reset_done.html
django.contrib.auth.PasswordResetDoneView
accounts/password_reset/done/ [name='password_reset_done']

regisration/password_reset_confirm.html  # "form" object to change password post email
django.contrib.auth.PasswordResetConfirmView
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']

registration/password_reset_done.html   # what shows after email reset
django.contrib.auth.PasswordResetCompleteView
accounts/reset/done/ [name='password_reset_complete']
"""
