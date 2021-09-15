from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from . models import Profile, Event, NewsLetter

from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template import Context

@receiver(post_save, sender = User)
def create_profile(sender, instance, created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("profile created")


@receiver(post_save, sender = Event)
def create_event(sender, instance,created,**kwargs):
    if created:
        nls = NewsLetter.objects.all()

        email_list = []
        for nl in nls:
            email_list.append(nl.email)
        event = instance
        subject ="Hey!! New Event Just Showed Up !! "
        c = {'sub':subject,'event':event.title, 'pk':event.pk, 'image':event.poster.url }
        text_content = render_to_string('email_templates/email.txt', c)
        html_content = render_to_string('email_templates/email_for_nl.html', c)

        email = EmailMultiAlternatives(subject, text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = email_list
        
        email.send()
        print("Email sent")

        