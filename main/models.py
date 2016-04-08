from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Page(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100, unique=True)
    add_date = models.DateField()
    order = models.IntegerField(unique=True)
    pic = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20)
    access = models.CharField(max_length=20)
    added_by = models.CharField(max_length=30, null=True)
    text = models.CharField(max_length=1000, null=True)
    tags = models.ManyToManyField(Tag)

class Paragraph(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000, null=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.IntegerField()

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    ip_address = models.CharField(max_length=30)
    add_date = models.DateTimeField()
    answer = models.CharField(max_length=500, null=True)

def generate_filename(instance, filename):
    url = 'profile_pics/%s/%s' % (instance.user_id, filename)
    return url

class Question(models.Model):
    text = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    answer_count = models.IntegerField()

class Answer(models.Model):
    text = models.CharField(max_length=100)
    votes_count = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.FileField(upload_to=generate_filename, null=True)
    phone = models.CharField(max_length=20, null=True)
    phone_show = models.CharField(max_length=3, null=True)
    about = models.CharField(max_length=300, null=True)
    about_show = models.CharField(max_length=3, null=True)
    city = models.CharField(max_length=50, null=True)
    city_show = models.CharField(max_length=3, null=True)
    email_show = models.CharField(max_length=3, null=True)
    groupname = models.CharField(max_length=20)
    votes = models.ManyToManyField(Question)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.CharField(max_length=30)
    text = models.CharField(max_length=500)
    date = models.DateTimeField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

class Mail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    text = models.CharField(max_length=500)
    date = models.DateTimeField()