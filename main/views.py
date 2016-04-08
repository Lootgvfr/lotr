from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import re
from datetime import date, datetime
from main.models import Page, Paragraph, Message, Profile, Tag, Question, Answer, Comment, Mail
from ipware.ip import get_ip
import random, string
from django.http import Http404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from main.forms import ImageForm

def get_pages(request, tag):
    """Return the list of pages tagged by the given tag."""
    pages_list = []
    if tag == '':
        pages = Page.objects.all().order_by('order')
    else:
        pages = Page.objects.filter(tags__name=tag).order_by('order')
    for p in pages:
        tags = []
        for tag in p.tags.all():
            tags.append(tag.name)
        po = {'url':p.url, 'page_title':p.title, 'text':p.text, 'pic':p.pic, 'date':str(p.add_date), 'paragraphs':[], 'access':p.access, 'status':p.status, 'author':p.added_by, 'tags':tags, 'comments':len(Comment.objects.filter(page=p))}
        pars = Paragraph.objects.filter(page=p).order_by('order')
        for par in pars:
            po['paragraphs'].append({'title':par.title, 'text':par.text, 'id':par.order})
        if accessable(p, request):
            pages_list.append(po)
    return pages_list

def get_tag_list():
    """Return a list of all tags."""
    tags = Tag.objects.all()
    res = []
    for tag in tags:
        name = tag.name
        count = tag.page_set.count()
        if count > 0:
            res.append({'name':name, 'count':count})
    res.sort(key=lambda x: x['count'], reverse=True)
    return res


def get_info(request):
    """Return the group name of a current user."""
    if not request.user.is_authenticated():
        return ''
    prf = Profile.objects.get(user = request.user)
    return prf.groupname

def get_questions(request):
    """Return the list of all polls and their results."""
    questions = Question.objects.all()
    res = []
    for question in questions:
        answered = 'yes'
        if request.user.is_authenticated():
            if len(Profile.objects.filter(user=request.user, votes__id=question.id)) == 0:
                answered = 'no'
        answers = []
        i = 0
        for answer in Answer.objects.filter(question=question):
            i += 1
            answers.append({'text':answer.text, 'votes_count':answer.votes_count, 'num':i})
        res.append({'name':question.name,'text':question.text,'answer_count':question.answer_count,'answered':answered,'answers':answers,'id':question.id})
    return res

def get_comments(request, page_name):
    """Return all comments to the given page."""
    pg = Page.objects.get(url=page_name)
    comments = Comment.objects.filter(page=pg).order_by('-date')
    res = []
    for comment in comments:
        username = User.objects.get(id=comment.user_id).username
        profile = Profile.objects.get(user=comment.user)
        if profile.img:
            profile_pic = profile.img.url
        else:
            profile_pic = ''
        res.append({'username':username, 'profile_pic':profile_pic, 'text':comment.text, 'ip':comment.ip, 'date':comment.date, 'id':comment.id})
    return res

def get_messages(request, type, search):
    """
    Return the list of messages for current user with options.
    
    Arguments:
    type -- 'received' or 'sent' messages
    search -- username to search
    """
    if search == '':
        if type == 'received':
            messages = Mail.objects.filter(receiver=request.user).order_by('-date')
        else:
            messages = Mail.objects.filter(sender=request.user).order_by('-date')
    else:
        if len(User.objects.filter(username=search)) > 0:
            if type == 'received':
                messages = Mail.objects.filter(receiver=request.user, sender=User.objects.get(username=search)).order_by('-date')
            else:
                messages = Mail.objects.filter(sender=request.user, receiver=User.objects.get(username=search)).order_by('-date')
        else:
            messages = []
    res = []
    if type=='received':
        for message in messages:
            prf = Profile.objects.get(user=message.sender)
            if prf.img:
                img = prf.img.url
            else:
                img = ''
            res.append({'username':message.sender.username, 'date':message.date, 'id':message.id, 'text':message.text, 'profile_pic':img})
    else:
        for message in messages:
            prf = Profile.objects.get(user=message.receiver)
            if prf.img:
                img = prf.img.url
            else:
                img = ''
            res.append({'username':message.receiver.username, 'date':message.date, 'id':message.id, 'text':message.text, 'profile_pic':img})
    return res


def accessable(page, request):
    """
    Check if current user can access given page.
    
    Arguments:
    page -- page object
    """
    if not request.user.is_authenticated():
        if page.access == 'user':
            return False
        return True
    else:
        prf = Profile.objects.get(user=request.user)
        grp = prf.groupname
        if page.status == 'hidden' and (grp == 'User' or grp == 'Moderator'):
            return False
        if page.status == 'hidden' and grp == 'Author' and page.added_by != request.user.username:
            return False
        return True

def index(request):
    """Main page."""
    grp = get_info(request)
    template = loader.get_template('main/main.html')
    context = RequestContext(request, {
        'group':grp
    })
    return HttpResponse(template.render(context))

def thx(request, name='default name'):
    """Page after leaving feedback."""
    grp = get_info(request)
    template = loader.get_template('main/thx.html')
    context = RequestContext(request, {
        'name':name,
        'group':grp
    })
    return HttpResponse(template.render(context))

def pages(request):
    """Page with all articles."""
    grp = get_info(request)
    questions = get_questions(request)
    tags = get_tag_list()
    pages_list = get_pages(request, '')
    if request.method == 'POST':
        try:
            id = int(request.POST['question_select'])
            ans = int(request.POST['radio'+str(id)])
            q = Question.objects.get(id=id)
            prf = Profile.objects.get(user=request.user)
            prf.votes.add(q)
            ans = Answer.objects.filter(question=q)[ans-1]
            ans.votes_count += 1
            ans.save()
            prf.save()
            return HttpResponseRedirect(reverse('pages'))
        except Exception as ex:
            print(ex)
    template = loader.get_template('main/pages.html')
    context = RequestContext(request, {
        'pages_list':pages_list,
        'group':grp,
        'tags':tags,
        'questions':questions
    })
    return HttpResponse(template.render(context))

def filter_pages(request, tag):
    """Page with filtered articles."""
    grp = get_info(request)
    questions = get_questions(request)
    tags = get_tag_list()
    if len(Tag.objects.filter(name=tag)) < 1:
        return HttpResponseRedirect(reverse('pages'))
    pages_list = get_pages(request, tag)
    template = loader.get_template('main/pages.html')
    context = RequestContext(request, {
        'pages_list':pages_list,
        'group':grp,
        'tags':tags,
        'questions':questions
    })
    return HttpResponse(template.render(context))

def page(request, page_name):
    """Page with an article."""
    grp = get_info(request)
    if len(page_name) > 4:
        if page_name[-4:] == '.xml':
            if len(Page.objects.filter(url=page_name[:-4])) > 0:
                p = Page.objects.get(url=page_name[:-4])
                t = loader.get_template('main/base.xml')
                c = Context({
                    'title':p.title,
                    'link':request.build_absolute_uri(reverse('pages', args=(p.url,))),
                    'date':p.add_date,
                    'description':p.text[:100]+'...'
                })
                return HttpResponse(t.render(c), content_type="text/xml")
    if request.method == 'POST':
        try:
            text = request.POST['text']
            submit_date = datetime.now()
            user_ip = get_ip(request)
            pg = Page.objects.get(url=page_name)
            com = Comment(user=request.user, text=text, date=submit_date, ip=user_ip, page=pg)
            com.save()
        except Exception as ex:
            print(ex)
        return HttpResponseRedirect(reverse('page', args=(page_name,)))
    else:
        pages_list = get_pages(request, '')
        urls = [page['url'] for page in pages_list]
        if page_name in urls:
            page = pages_list[urls.index(page_name)]
        else:
            raise Http404()
        comments = get_comments(request, page_name)
        template = loader.get_template('main/text.html')
        context = RequestContext(request, {
            'selected_page':page,
            'group':grp,
            'comments':comments
        })
        return HttpResponse(template.render(context))

def del_comment(request, page_name, id):
    """Delete comment and redirect to same page."""
    if len(Comment.objects.filter(id=id)) == 0:
        return HttpResponseRedirect(reverse('page',args=(page_name,)))
    com = Comment.objects.get(id=id)
    if get_info(request) == 'Admin' or get_info(request) == 'Moderator' or (get_info(request) == 'User' and request.user == com.user):
        com.delete()
    return HttpResponseRedirect(reverse('page',args=(page_name,)))

def rss(request):
    """RSS feed."""
    t = loader.get_template('main/rss.xml')
    pages = []
    ps = Page.objects.filter(status='published')
    for page in ps:
        pages.append({'title':page.title, 'link':request.build_absolute_uri(reverse('page', args=(page.url,))), 'date':page.add_date, 'description':page.text[:100]+'...'})
    c = Context({
        'pages':pages
    })
    return HttpResponse(t.render(c), content_type="text/xml")

def form(request):
    """Page with feedback form."""
    grp = get_info(request)
    error = ''
    name = ''
    email = ''
    message = ''
    ans = 'no'
    answers = []
    if request.user.is_authenticated():
        name = request.user.first_name
        email = request.user.email
        msgs = Message.objects.filter(name=request.user.first_name)
        for msg in msgs:
            if msg.answer != '':
                answers.append({'message':msg.text, 'answer':msg.answer})
        if len(answers) > 0:
            ans = 'yes'
    if request.method == "POST":
        try:
            name = request.POST['Name']
            email = request.POST['Email']
            message = request.POST['Message']
            em = re.compile(r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$')
            if name == '' or email == '' or message == '' or name == 'Name' or message == 'Your message':
                raise Exception('Some of the fields are empty.')
            elif len(name) > 29:
                raise Exception('Name is too long.')
            elif not em.match(email):
                raise Exception('Email is not valid.')
            elif len(message) < 6:
                raise Exception('Your message is too short.')       
        except Exception as ex:
            error = ex
        else:
            submit_date = datetime.now()
            user_ip = get_ip(request)
            if request.user.is_authenticated():
                usr = User.objects.get(username = request.user.username)
                usr.first_name = name
                usr.save()
            sub = Message(name = name, email = email, text = message, ip_address = str(user_ip), add_date=submit_date)
            sub.save()
            return HttpResponseRedirect(reverse('thx', args=(name,)))
    return render(request, 'main/form.html', {
        'error_message':error,
        'name':name,
        'email':email,
        'message':message,
        'ans':ans,
        'answers':answers,
        'group':grp
    })
    
def page404(request):
    """Page with 404 error."""
    grp = get_info(request)
    template = loader.get_template('main/404.html')
    context = RequestContext(request, {
        'group':grp
    })
    return HttpResponse(template.render(context))

def login(request):
    """Page with login form."""
    grp = get_info(request)
    if request.user.is_authenticated():
        auth_logout(request)
    error = ''
    username = ''
    if request.method == "POST":
        try:
            username = request.POST['Username']
            password = request.POST['Password']
            user = authenticate(username=username, password=password)
            if user is None:
                raise Exception('Invalid login data')
            else:
                if not user.is_active:
                    raise Exception('This user is disabled')
        except Exception as ex:
            error = ex
            password_error = True
        else:
            auth_login(request, user)   
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'main/login.html', {
        'error_message':error,
        'username':username,
        'group':grp
    })

def register(request):
    """Page with registration form."""
    grp = get_info(request)
    if request.user.is_authenticated():
        auth_logout(request)
    error = ''
    username = ''
    email = ''
    if request.method == "POST":
        try:
            username = request.POST['Username']
            email = request.POST['Email']
            password = request.POST['Password']
            pr = request.POST['Password_repeat']
            em = re.compile(r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$')
            n = re.compile(r'^[a-zA-Z0-9_@+.-]+$')
            if username == '' or email == '' or password == '' or pr == '':
                raise Exception('Some of the fields are empty.')
            elif len(username) > 29:
                raise Exception('Username too long.')
            elif not n.match(username):
                raise Exception('Username contains unallowed characters (only alphanumeric, _, @, +, . and - are allowed)')
            elif not em.match(email):
                raise Exception('Email is not valid.')
            elif password != pr:
                raise Exception('Passwords do not match.')       
        except Exception as ex:
            error = ex
        else:
            user = User.objects.create_user(username, email, password)
            prf = Profile(user = user, groupname = 'User', email_show='no', city_show='no', phone_show='no', about_show='no', city='', phone='', about='')
            prf.save()
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'main/register.html', {
        'error_message':error,
        'username':username,
        'email':email,
        'group':grp
    })

def logout(request):
    """Log out and redirect to home."""
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))

def no_access(request):
    """Page with no access error."""
    grp = get_info(request)
    template = loader.get_template('main/no_access.html')
    context = RequestContext(request, {
        'group':grp
    })
    return HttpResponse(template.render(context))

def profile(request, username):
    """Page with user profile."""
    grp = get_info(request)
    if len(User.objects.filter(username=username))>0:
        us = User.objects.get(username=username)
        prf = Profile.objects.get(user=us)
        template = loader.get_template('main/profile.html')
        context = RequestContext(request, {
            'profile':prf,
            'group':grp,
            'sel_user':us
        })
        return HttpResponse(template.render(context))
    else:
        raise Http404()

def edit_profile(request, username):
    """Page with form for editing profile."""
    if not request.user.is_authenticated():
        raise Http404()
    grp = get_info(request)
    if len(User.objects.filter(username=username)) == 0:
        raise Http404()
    usr = User.objects.get(username=username)
    prf = Profile.objects.get(user=usr)
    error = ''
    name = usr.first_name
    email = usr.email
    form = ImageForm()
    if request.method == "POST":
        if 'save' in request.POST:
            try:
                name = request.POST['name']
                email = request.POST['email']
                city = request.POST['city']
                phone = request.POST['phone']
                about = request.POST['about']
                email_show = request.POST['email_show']
                city_show = request.POST['city_show']
                phone_show = request.POST['phone_show']
                about_show = request.POST['about_show']
                em = re.compile(r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$')
                ph = re.compile(r'\+?[0-9]+$')
                if email == '':
                    raise Exception("Email field can't be empty.")
                elif len(phone)>0 and not ph.match(phone):
                    raise Exception('Phone number is not valid.')
                elif not em.match(email):
                    raise Exception('Email is not valid.') 
            except Exception as ex:
                error = ex
            else:
                user = User.objects.get(username=username)
                user.first_name = name
                user.email = email
                prf = Profile.objects.get(user=user)
                prf.phone = phone
                prf.city = city
                prf.about = about
                prf.city_show = city_show
                prf.phone_show = phone_show
                prf.about_show = about_show
                prf.email_show = email_show
                prf.save()
                user.save()
                return HttpResponseRedirect(reverse('profile', args=(username,)))
        else:
            try:
                form = ImageForm(request.POST, request.FILES)
                if not form.is_valid():
                    raise Exception('Помилка завантаження файлу.')
            except Exception as ex:
                error = ex
            else:
                user = User.objects.get(username=username)
                prf = Profile.objects.get(user=user)
                prf.img = request.FILES['img']
                prf.save()
                return HttpResponseRedirect(reverse('profile', args=(username,)))
    return render(request, 'main/edit_profile.html', {
        'form':form,
        'error_message':error,
        'username':username,
        'name':name,
        'profile':prf,
        'email':email,
        'group':grp
    })

def del_pic(request, username):
    """Delete profile picture and redirect to profile."""
    if not request.user.is_authenticated():
        raise Http404()
    grp = get_info(request)
    if len(User.objects.filter(username=username)) == 0:
        raise Http404()
    usr = User.objects.get(username=username)
    prf = Profile.objects.get(user=usr)
    prf.img.delete()
    prf.img = None
    prf.save()
    return HttpResponseRedirect(reverse('profile', args=(username,)))

def change_group(request, username):
    """Change group of a user and redirect to profile."""
    if request.method == 'POST':
        try:
            prf = Profile.objects.get(user=User.objects.get(username=username))
            prf.groupname = request.POST['group']
            prf.save()
        except Exception as ex:
            print(ex)
        return HttpResponseRedirect(reverse('profile', args=(username,)))
    else:
        return HttpResponseRedirect(reverse('profile', args=(username,)))

def mailbox(request):
    """Redirect to received messages."""
    return HttpResponseRedirect(reverse('mailbox_received'))

def mailbox_received(request):
    """Page with received messages."""
    grp = get_info(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('no_access'))
    if request.method == 'POST':
        try:
            username = request.POST['Username']
            return HttpResponseRedirect(reverse('mailbox_received_search', args=(username,)))
        except Exception as ex:
            print(ex)
    messages = get_messages(request, 'received', '')
    template = loader.get_template('main/mailbox.html')
    context = RequestContext(request, {
        'group':grp,
        'mails':messages,
        'type':'received'
    })
    return HttpResponse(template.render(context))

def mailbox_received_search(request, username):
    """Page with filtered received messages."""
    grp = get_info(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('no_access'))
    messages = get_messages(request, 'received', username)
    template = loader.get_template('main/mailbox.html')
    context = RequestContext(request, {
        'group':grp,
        'type':'received',
        'mails':messages
    })
    return HttpResponse(template.render(context))

def mailbox_sent(request):
    """Page with sent messages."""
    grp = get_info(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('no_access'))
    if request.method == 'POST':
        try:
            username = request.POST['Username']
            return HttpResponseRedirect(reverse('mailbox_sent_search', args=(username,)))
        except Exception as ex:
            print(ex)
    messages = get_messages(request, 'sent', '')
    template = loader.get_template('main/mailbox.html')
    context = RequestContext(request, {
        'group':grp,
        'type':'sent',
        'mails':messages
    })
    return HttpResponse(template.render(context))

def mailbox_sent_search(request, username):
    """Page with filtered sent messages."""
    grp = get_info(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('no_access'))
    messages = get_messages(request, 'sent', username)
    template = loader.get_template('main/mailbox.html')
    context = RequestContext(request, {
        'group':grp,
        'type':'sent',
        'mails':messages
    })
    return HttpResponse(template.render(context))

def mailbox_send(request):
    """Page with message sending form."""
    grp = get_info(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('no_access'))
    error = ''
    to = ''
    text = ''
    if request.method == "POST":
        try:
            to = request.POST['to']
            text = request.POST['text']
            if to == '' or text == '':
                raise Exception('Enter receiver and message text')
            if len(User.objects.filter(username=to)) == 0:
                raise Exception('User with this name was not found.')
        except Exception as ex:
            error = ex
        else:
            mail = Mail(sender=request.user, receiver=User.objects.get(username=to), date=datetime.now(), text=text)
            mail.save()
            return HttpResponseRedirect(reverse('mailbox_sent'))
    return render(request, 'main/mailbox_send.html', {
        'error_message':error,
        'to':to,
        'text':text,
        'group':grp
    })

def mailbox_send_to(request, to):
    """Page with message sending form with preset user."""
    grp = get_info(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('no_access'))
    template = loader.get_template('main/mailbox_send.html')
    context = RequestContext(request, {
        'group':grp,
        'to':to
    })
    return HttpResponse(template.render(context))

def mailbox_del(request, id):
    """Delete message and redirect to mailbox."""
    grp = get_info(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('no_access'))
    if len(Mail.objects.filter(id=id)) > 0:
        ml = Mail.objects.get(id=id)
        if ml.receiver == request.user:
            ml.delete()
    return HttpResponseRedirect(reverse('mailbox_received'))