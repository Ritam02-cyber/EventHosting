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
]