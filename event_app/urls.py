from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name="home"),
    path('add_event', views.add_event, name="add_event"),
    path('add_form_parent/<int:pk>', views.add_form_parent, name="add_form_parent"),
    path('add_form_fields/<int:pk>', views.add_form_fields, name="add_form_fields"),
    path('delete_form_field/<int:pk>', views.delete_form_field, name='delete_form_field'),
    path('event_view_host/<int:pk>', views.event_view_host, name='event_view_host'),
    path('responses/<int:pk>', views.responses, name='responses'),
    path('event_home/<int:pk>', views.event_home, name='event_home'),
    path('form_view/<str:unique_id>', views.form_view, name='form_view'),
    path('form_submit/<str:unique_id>', views.form_submit,name="form_submit"),
    path('accept_responses_toggle/<int:pk>', views.accept_responses_toggle, name='accept_responses_toggle'),
    path('all_events_view_host', views.all_events_view_host, name='all_events_view_host'),
    path('winner_declaration/<str:unique_id>', views.winner_declaration, name='winner_declaration'),
    path('send_mail_to_winners/<str:unique_id>', views.send_mail_to_winners, name='send_mail_to_winners'),
    path('send_mail_to_participants/<str:unique_id>', views.send_mail_to_participants, name='send_mail_to_participants'),
    path('register_home', views.register_home, name='register_home'),
    path('log_in', views.log_in, name='log_in'),
]