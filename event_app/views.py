from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import Http404, JsonResponse
from . models import *
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
import pytz
from datetime import datetime
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string




# Create your views here.
def convert_time(time):
    time = time[:-5]
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")



def home(request):
    events = Event.objects.filter(status= True, restricted = False, ).order_by('-created_time')[:5]
    event_list =[]
    for event in events:
        # print(event)
        winning_positions = WinningPosition.objects.filter(event_of = event)
        if len(winning_positions) == 0:
            print(event)
            event_list.append(event)

    groups = EventGroup.objects.all()
    context ={
        'events':event_list,
        'groups':groups,
    }
    return render(request, 'home.html', context)


def all_events(request):
    current_events = Event.objects.filter(result_out =False).order_by('-created_time')
    past_events = Event.objects.filter(result_out= True).order_by('-created_time')
    context = {'current_events':current_events, 'past_events':past_events}
    return render(request, 'applicant_view/all_events_view.html', context)

def all_groups(request):
    groups = EventGroup.objects.all()
    context = {'groups':groups}
    return render(request, 'applicant_view/all_groups_view.html', context)

def group_view(request, pk):
    group = get_object_or_404(EventGroup, pk=pk)
    past_events = Event.objects.filter(result_out = True, group=group)
    current_events = Event.objects.filter(result_out= False, group=group)
    context ={
        'group':group,
        'past_events':past_events,
        'current_events':current_events,
    }
    return render(request, 'group_view.html', context)

def form_view(request, unique_id):
    
    form_parent_obj = get_object_or_404(FormParent, unique_id=unique_id)
    if form_parent_obj.event_obj.end_time < datetime.now(timezone.utc):
        return redirect('/event_home/' + str(form_parent_obj.event_obj.pk))
    form_designs = FormDesign.objects.filter(form_parent=form_parent_obj)
    formobj = FormObject.objects.filter(form_parent=form_parent_obj, applicant = request.user.profile)
    context ={
        'form_parent':form_parent_obj,
        'form_designs':form_designs,
        'formobj':formobj
    }
    
    
    return render(request, 'applicant_view/form_view.html', context)





def event_home(request, pk):
   

    event = get_object_or_404(Event, pk=pk)
    winner_positions = WinningPosition.objects.filter(event_of=event)
    event_form_parent = FormParent.objects.filter(event_obj = event)
    start_time = event.start_time.strftime("%Y-%m-%d %H:%M:%S")
    print(start_time)
    print(event.no_of_participants)
    print(len(event.participants.all()))
    if event.no_of_participants <= len(event.participants.all()):
        print("No participants max")
        context = {
            'event': event,
            'started':True,
            
            
            'max_reached':True,
            'winner_positions':winner_positions
        }



   
    elif event.start_time < datetime.now(timezone.utc) and event.end_time > datetime.now(timezone.utc):
        print('started, not ended')
        # event_form_parent = get_object_or_404(FormParent, event_obj = event)
        
        context = {
            'event': event,
            'start_time':start_time,
            'event_form':event_form_parent,
            'started':True,
            'winner_positions':winner_positions
        }
    elif event.start_time > datetime.now(timezone.utc):
        print('not started')
        context={
            'event': event,
            'start_time':start_time,
            'event_form':event_form_parent,
            'not_started':True,
            'winner_positions':winner_positions
        }
    elif event.end_time < datetime.now(timezone.utc):
        print('ended') 
        context = {
            'event':event,
            'start_time':start_time,
            'ended':True,
            'winner_positions':winner_positions
        }
    return render(request, 'applicant_view/event_home.html', context)




def form_submit(request, unique_id):
    form_parent_obj = get_object_or_404(FormParent, unique_id=unique_id)
    form_designs = FormDesign.objects.filter(form_parent=form_parent_obj)
    profile = get_object_or_404(Profile, user = request.user)
    form_obj = FormObject(
        form_parent = form_parent_obj,
        applicant = profile

    )
    form_obj.save()
    # print("kk")
    start_time = form_parent_obj.event_obj.start_time
    end_time = form_parent_obj.event_obj.end_time
    event = form_parent_obj.event_obj
    if event.no_of_participants <= len(event.participants.all()):
        return redirect('/form_view/' + str(unique_id))
    if form_parent_obj.accept_responses == False:
        return redirect('/form_view/' + str(unique_id))
    if event.start_time < datetime.now(timezone.utc) and event.end_time > datetime.now(timezone.utc):
        print('started, not ended')
    


        if request.method == 'POST':
            for field in form_designs:
                if field.character_field:
                    # print(field.pk)
                    form_char_obj = FormCharacterField(
                        field_data = request.POST.get(str(field.pk)),
                        form_object = form_obj,
                        label_name = request.POST.get('char' + str(field.pk))  
                    )
                    form_char_obj.save()
                elif field.big_text_field:
                    form_txt_field = FormBigTextField(
                        field_data = request.POST.get(str(field.pk)),
                        form_object = form_obj, 
                        label_name = request.POST.get('txt' + str(field.pk))

                    )
                    form_txt_field.save()
                elif field.integer_field:
                    form_int_field = FormIntegerField(
                        field_data = request.POST.get(str(field.pk)),
                        form_object = form_obj,
                        label_name = request.POST.get('int' + str(field.pk)) 

                    )
                    form_int_field.save()
                elif field.file_field:

                    form_file_field = FormFileField(
                        field_data = request.FILES[str(field.pk)],
                        form_object = form_obj, 
                        label_name = request.POST.get('file' + str(field.pk))

                    )
                    form_file_field.save()
                elif field.mcq_field:
                    choices = field.choice_set.all()
                    checked = request.POST.get('flexRadioDefault' + str(field.pk))
                    # print(checked)
                    form_mcq_field = MCQField(
                    field_data = checked,
                    form_object = form_obj,
                    label_name = request.POST.get('mcq' + str(field.pk)),
                    form_design = field
                    
                    )
                    # form_mcq_field.form_design.add(field)
                    form_mcq_field.save()
            event.participants.add(profile)
            return redirect('/form_view/' + str(unique_id))
    elif event.start_time > datetime.now(timezone.utc):
        print("not started")
    
        context ={
            'error':'Sorry!! Event is not started yet',
            'event': event,
            'form_parent':form_parent_obj
        }
        return render(request, 'applicant_view/form_submit_error.html',context)
    elif event.end_time < datetime.now(timezone.utc):
        print("ended")
        
        context ={
            'error':'Event ended',
            'event': event,
            'form_parent':form_parent_obj
        }
        return render(request, 'applicant_view/form_submit_error.html',context)

def add_group(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        poster = request.FILES.get('poster', '')
        if poster != '':
            group = EventGroup(name=name, description=description, poster=poster, creator = request.user.profile)
        else:
            group = EventGroup(name=name, description=description,  creator = request.user.profile)
        group.save()
        return redirect('/add_event')






def add_event(request):
    events = Event.objects.all()
    groups = EventGroup.objects.all()
    
    if request.method == 'POST':

        name = request.POST.get('name', '')
        description = request.POST.get('description','')
        rules = request.POST.get('rules', '')
        poster = request.FILES.get('poster', '')

        no_of_participants= request.POST.get('no_of_participants', '')
        type_ = request.POST.get('type', '')
        restriction = request.POST.get('restriction', '')
        print(restriction)
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')
        tags = request.POST.get('tags', '')
        group = request.POST.get('group', '')
        print(start_time)
        print(end_time)
        print(tags)

       
        prof = Profile.objects.filter(user = request.user)[0]
  
        if poster != '' and group != '':
            event = Event(
                title = name,
                description = description,
                rules = rules, 
                poster = poster,
                type_of = type_, 
                restricted = restriction,
                host = prof, 
                no_of_participants=no_of_participants, 
                start_time=start_time, 
                end_time=end_time, 
                group=EventGroup.objects.filter(pk = group)[0]
           
                )
        elif poster == '' and group =='':
            event = Event(
                title = name,
                description = description,
                rules = rules, 
                # poster = poster,
                type_of = type_, 
                restricted = restriction,
                host = prof, 
                no_of_participants=no_of_participants, 
                start_time=start_time, 
                end_time=end_time, 
               
                )
        elif poster !='' and group =='':
            event = Event(
                title = name,
                description = description,
                rules = rules, 
                # poster = poster,
                type_of = type_, 
                restricted = restriction,
                host = prof, 
                no_of_participants=no_of_participants, 
                start_time=start_time, 
                end_time=end_time, 
                poster = poster,
               
                )
        elif poster == '' and group != '':
            event = Event(
                title = name,
                description = description,
                rules = rules, 
                # poster = poster,
                type_of = type_, 
                restricted = restriction,
                host = prof, 
                no_of_participants=no_of_participants, 
                start_time=start_time, 
                end_time=end_time, 
                group=EventGroup.objects.filter(pk = group)[0]
                )

        event.save()

        # tagging
        tags = tags.split(',')
        print(tags)
        for tag in tags:
            tag = tag.replace(" ", "")
            tag = tag.upper()
            tag_obj = Tag.objects.filter(name = tag)
            if tag_obj:
                tag_obj[0].event.add(event)
                # tag_obj.save()
            else:
                obj = Tag(name = tag)
                obj.save()
                obj.event.add(event)
                

            print(tag)
        return redirect('/add_form_parent/' + str(event.id))

    context = {
        'events': events,
        'groups': groups,

    }
    return render(request, "add_event.html", context)


def add_form_parent(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':

        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        banner = request.FILES.get('banner')
        # print(banner)
        event = get_object_or_404(Event, pk=pk)
        if banner is not None:
            form_parent_obj = FormParent(title=title, description=description,  banner_img = banner, event_obj = event)
        else:
            form_parent_obj = FormParent(title=title, description=description, event_obj= event)
      
        form_parent_obj.save()
        
        return redirect('/add_form_fields/' + str(form_parent_obj.pk))
    
    return render(request, 'add_form_home.html', {'event':event})



# @login_required(login_url='/login_page')
def add_form_fields(request, pk):
    form_parent_obj =get_object_or_404(FormParent,id=pk)
    form_designs = FormDesign.objects.filter(form_parent=form_parent_obj)
    formobjs = FormObject.objects.filter(form_parent=form_parent_obj)
    if request.method == 'POST':
        label_name = request.POST.get('label_name', '')
        field_type = request.POST.get('field_type', '')
        
        # print(label_name)
        # print(field_type)
        if field_type == 'CF':
            form_design_obj = FormDesign(
                label=label_name,
                character_field = True,
                form_parent=form_parent_obj

            )
            form_design_obj.save()
        elif field_type == 'TF':
            form_design_obj = FormDesign(
                label=label_name,
                big_text_field = True,
                form_parent=form_parent_obj
               
            )
            form_design_obj.save()
        elif field_type == 'IF':
            form_design_obj = FormDesign(
                label=label_name,
                integer_field = True,
                form_parent=form_parent_obj
              
            )
            form_design_obj.save()
        elif field_type == 'FF':
            form_design_obj = FormDesign(
                label=label_name,
                file_field = True,
                form_parent=form_parent_obj
             

            )
            form_design_obj.save()
        elif field_type == 'MF':
            options_value = request.POST.get('options_value', '')
            
            form_design_obj = FormDesign(
                label=label_name,
                mcq_field = True,
                form_parent=form_parent_obj
             

            )
            form_design_obj.save()
            for i in options_value.split(','):
                choice_obj = Choice(name=i, mcq_parent= form_design_obj)
                choice_obj.save()

        
    context = {
            'form_parent':form_parent_obj,
            'form_designs':form_designs,
            'formobjs':formobjs

        }

    return render(request, 'add_form_fields.html', context)



# @login_required(login_url='/login_page')
def delete_form_field(request, pk):
    form_field = get_object_or_404(FormDesign, pk=pk)
    form_parent = form_field.form_parent
    # print(form_field)

    if form_parent.event_obj.host == request.user.profile:
        form_field.delete()

    return redirect('/add_form_fields/' + str(form_parent.pk))
def event_view_host(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user == event.host.user:
        return render(request, 'event_view_host.html', {'event': event})
    else:
        raise Http404()




def responses(request, pk):
    form_parent = FormParent.objects.filter(pk =pk)
    data_dict ={}
    print(form_parent)
    if form_parent and request.user.profile == form_parent[0].event_obj.host:
        

        form_designs = FormDesign.objects.filter(form_parent = form_parent[0])
        formobjs = FormObject.objects.filter(form_parent = form_parent[0])
        
        for obj in formobjs:
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj] ={}
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['chars'] =[FormCharacterField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['txts'] =[ FormBigTextField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['ints'] =[ FormIntegerField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['files'] =[ FormFileField.objects.filter(form_object = obj)]
            data_dict['From ' + str(obj.applicant.user.username) + str(obj.pk),obj]['mcq'] =[ MCQField.objects.filter(form_object = obj)]
            
         

        mcq_design = FormDesign.objects.filter(form_parent = form_parent[0], mcq_field= True)
        if mcq_design:
            mcq_design = mcq_design[0]
        else:
            mcq_design =[]


        # print(data_dict)
        context={
            'data_dict':data_dict,
            'form_parent':form_parent,
            'mcq_design':mcq_design
        }
    else:
        # print("no form")
        context = {
            'data_dict':data_dict,
            
        }
        return redirect('/forms')

    return render(request,'responses.html', context)

def accept_responses_toggle(request, pk):
    if request.method == 'POST':
        data_from_post = json.load(request)['toggle_check']
        form_parent = get_object_or_404(FormParent, pk =pk)
        # print(data_from_post)
        form_parent.accept_responses = data_from_post
        form_parent.save()

        data = {
            'toggle_value':'toggle_value',
        }
        return JsonResponse(data)
    else:
        raise Http404()


# def all_events_view_host(request):
#     events = Event.objects.filter(host = request.user.profile)
#     context ={
#         'events': events,
#     }

#     return render(request,'all_events_view_host.html', context)

def winner_declaration(request, unique_id):
    event = get_object_or_404(Event, unique_id=unique_id)
    winner_positions = WinningPosition.objects.filter(event_of=event)
    if len(winner_positions) != 0:
        event.result_out =  True
        event.save()
    if request.method == 'POST':
        position_name = request.POST.get('position', '')
        profs = request.POST.getlist('profs', '')
        print(profs)
        print(position_name)
        winning_position_obj = WinningPosition(position_name=position_name, event_of=event)
        winning_position_obj.save()
        for i in profs:
            winning_position_obj.prof.add(get_object_or_404(Profile, pk =i))
        return redirect("/winner_declaration/" + str(event.unique_id))


    context = {
        'event': event,
        'winner_positions': winner_positions
        }
    return render(request,'winner_declaration.html', context)


def send_mail_to_winners(request, unique_id):
    event = get_object_or_404(Event, unique_id=unique_id)
    winning_positions = WinningPosition.objects.filter(event_of=event) 
    if request.method == 'POST':
        positions = request.POST.getlist('positions', [])
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        print(positions, subject, message)
        email_list =[]
        for i in positions:
            print(i)
            position_obj = get_object_or_404(WinningPosition, pk=i)
            for k in position_obj.prof.all():
                email_list.append(k.user.email)
        print(email_list)


        c = {'sub':subject,'message':message }
        text_content = render_to_string('email_templates/email.txt', c)
        html_content = render_to_string('email_templates/email.html', c)

        email = EmailMultiAlternatives(subject, text_content)
        email.attach_alternative(html_content, "text/html")
      
        email.to = email_list
        email.send()
        #email to winners
        # template_locator = render_to_string('Email_templates/email.html', {'sub':subject,'message':message })
        # email_locator = EmailMessage(
        #     subject,
        #     template_locator,
        #     settings.EMAIL_HOST_USER,
        #     email_list,

        #     )
        # email_locator.fail_silently = False
        # email_locator.send()
    context = {'event': event}
    return redirect('/winner_declaration/' + str(unique_id))

def send_mail_to_participants(request,unique_id):
    event = get_object_or_404(Event, unique_id=unique_id)

    if request.method == 'POST':
        participants = request.POST.getlist('participants', [])
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        print(participants)
        c = {'sub':subject,'message':message }
        text_content = render_to_string('email_templates/email.txt', c)
        html_content = render_to_string('email_templates/email.html', c)

        email = EmailMultiAlternatives(subject, text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = participants
        
        email.send()
    context = {'event': event}
    return render(request, 'send_mail_to_participants.html', context)

def register_home(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        conf_password = request.POST.get('conf_password', '')
        userCheck = User.objects.filter(username =username)
        type_of_account = request.POST.get('type_of_account')
        print(type_of_account)
        if len(username)> 20:
            messages.warning(request,"Too Long Username!!")
        elif password != conf_password:
            messages.warning(request, "Passwords Don't Match!!")
        elif userCheck:
            messages.warning(request, "Username Already Exists , Kindly Change!!")
        else:
            user_obj = User.objects.create_user(first_name = name, password = password, email = email, username=username)

            user_obj.save()
            # prf =Profile(prof_user= user_obj)
            # prf.save()
            prof = get_object_or_404(Profile, user = user_obj)
            prof.type_of = type_of_account
            prof.save()

            messages.success(request, "Account Created Successfully!!")
    
    return render(request, 'register_home.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user_obj = authenticate( username= username, password = password)
        print(user_obj)
        if user_obj is not None:
            login(request, user_obj)
            messages.success(request, "Logged In Successfully :^) ")
            return redirect('/')
        else:
            messages.warning(request, "Invalid Credentials : ( ")
            return redirect('/register_home')
    else:
        raise Http404()

def leaderboard(request):
    profs = Profile.objects.all()
    data ={}
    for i in profs:
        data[i] = len(Event.objects.filter(participants = i))
    print(data)
    context ={
        'data': data,
    }
    return render(request, 'applicant_view/leaderboard.html', context)

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    events = Event.objects.filter(participants = user_obj.profile)
    context ={
        'user_obj':user_obj,
        'events':events,
    }
    return render(request, 'applicant_view/profile.html',context)
def events_list_host(request):
    events = Event.objects.filter(host= request.user.profile).order_by('-created_time')
    context = {
        'events':events,
    }

    return render(request, 'events_list_host.html', context)

def contact_host(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        c = {'sub':subject,'message':message }
        text_content = render_to_string('email_templates/email.txt', c)
        html_content = render_to_string('email_templates/email.html', c)

        email = EmailMultiAlternatives(subject, text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [event.host.user.email]
        
        email.send()

        return redirect('/event_home/' + str(event.pk))

def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user.profile == event.host:
        event.delete()
        return redirect('/events_list_host')

def log_out(request):
    logout(request)
    return redirect("/")    


