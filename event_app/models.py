from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
TYPE_OF_EVENT =[
    ('GM','Gaming'),
    ('NR','Normal')
]

TYPE_OF_PROFILE=[
    ('HS', 'Host'),
    ('NR', 'Normal')
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100,default=" ")
    type_of = models.CharField(max_length=2, choices=TYPE_OF_PROFILE,default='NR')
    def __str__(self):
        return str(self.user)

# class Participant(models.Model):
#     prof = models.OneToOneField(Profile, on_delete = models.CASCADE)
#     def __str__(self):
#         return str(self.prof.user.username)

class Event(models.Model):
    title = models.CharField(max_length=400)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    description = models.TextField(blank=True, null= True)
    poster = models.ImageField(upload_to= 'posters',default = 'banner.png')
    rules = models.TextField(blank=True, null=True)
    type_of = models.CharField(max_length=2, choices=TYPE_OF_EVENT,default='NR')
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    no_of_participants  = models.IntegerField(default=0, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(Profile, related_name="participants")
    status = models.BooleanField(default=True)
    restricted = models.BooleanField(default=False)
    result_out = models.BooleanField(default=False)
    def __str__(self):
        return str(self.title) + ' from ' + str(self.host)



class WinningPosition(models.Model):
    position_name = models.CharField(max_length=100)
    event_of = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    prof = models.ManyToManyField(Profile)
    def __str__(self):
        return str(self.prof) + ' won ' + str(self.position_name)



# form design


class FormParent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_obj = models.OneToOneField(Event, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    accept_responses = models.BooleanField(default=True)
    banner_img = models.ImageField(upload_to = 'banners', default='banner.png', blank=True, null=True)

    def __str__(self):
        return self.title


class FormDesign(models.Model):
    label= models.TextField()
    form_parent = models.ForeignKey(FormParent, on_delete=models.CASCADE)
    character_field = models.BooleanField(default = False)
    big_text_field = models.BooleanField(default = False)
    integer_field = models.BooleanField(default = False)
    file_field = models.BooleanField(default = False)
    mcq_field = models.BooleanField(default = False)
    def __str__(self):
        return self.form_parent.title





class FormObject(models.Model):
    form_parent = models.ForeignKey(FormParent, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.form_parent.title 

    
class FormCharacterField(models.Model):
    label_name = models.TextField(blank=True)
    field_data = models.CharField(max_length=400)
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="char")

    def __str__(self):
        return self.form_object.form_parent.title

class FormBigTextField(models.Model):
    label_name = models.TextField(blank=True)
    field_data = models.TextField()
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="txt")
    def __str__(self):
        return self.form_object.form_parent.title


class FormIntegerField(models.Model):
    label_name = models.TextField(blank=True)
    field_data = models.BigIntegerField()
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="int")
    def __str__(self):
        return self.form_object.form_parent.title

class FormFileField(models.Model):
    label_name = models.TextField( blank=True)
    field_data = models.FileField(upload_to='fileData')
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="file")
    def __str__(self):
        return self.form_object.form_parent.title





class MCQField(models.Model):
    label_name = models.TextField(blank=True)
    field_data = models.IntegerField()
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="Single")
    form_design = models.ForeignKey(FormDesign, on_delete=models.CASCADE)
    def __str__(self):
        return self.form_object.form_parent.title

class Choice(models.Model):
    name = models.CharField(max_length=100)
    mcq_parent = models.ForeignKey(FormDesign, on_delete= models.CASCADE)
    def __str__(self):
        return self.name


