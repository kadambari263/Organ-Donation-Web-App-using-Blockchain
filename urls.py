from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from home.view.home import home
from home.view import register_view,login_view,logout_view,donor_register,receiver_register,receiver_list,download_receivers,receiver_edit,receiver_result,profile_view,edit_profile_view,send_request_email,send_request_email_view
from home.view.contact import contact_page, contact_submit
from home.view.about import about
from home.view import result
from django.contrib.auth import views as auth_views

from home.view.dev import dev_view

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('donor/register/', donor_register, name='donor_register'),
    path('donor/success/', lambda r: render(r, 'doner/success.html'), name='donor_success'),

    path('receiver/register/', receiver_register, name='receiver_register'),
    path('receiver/list/', receiver_list, name='receiver_list'),
    path('receiver/download/', download_receivers, name='download_receivers'),
    path('edit/<int:pk>/', receiver_edit, name='receiver_edit'),
    path('receiver/result/<int:pk>/', receiver_result, name='receiver_result'),

    
    path('contact/', contact_page, name='contact_page'),
    path('contact/submit/', contact_submit, name='contact_submit'),

    path('about/', about, name='about'),

    path('developers/', dev_view, name='developers'),

    path('receiver/<int:receiver_id>/result/', result.result_view, name='result'),
    path('match/<int:match_id>/approve/', result.approve_match, name='approve_match'),

    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('send-request-email/', send_request_email_view, name='send_request_email'),
    

     # Password reset - send reset email
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset_form.html'), name='password_reset'),

    # Password reset done (email sent confirmation)
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),

    # Password reset confirm (link with token)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),

    # Password reset complete (success message after reset)
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

    # Optional: Password change for logged-in users
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='auth/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'),
]
    
