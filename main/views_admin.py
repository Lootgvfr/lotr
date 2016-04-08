from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
import re
from datetime import date, datetime
from main.models import Page, Paragraph, Message, Profile, Tag, Question, Answer
from ipware.ip import get_ip
import random, string
from django.http import Http404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group

def admin_index(request):
    """Redirect to article managing."""
    return HttpResponseRedirect(reverse('admin_pages'))

def get_info(request):
    """Return groupname of a current user."""
    if not request.user.is_authenticated():
        return ''
    prf = Profile.objects.get(user = request.user)
    return prf.groupname

def no_access(request, page):
    """Page with no access error."""
    if not request.user.is_authenticated():
        return True
    u = request.user
    prof = Profile.objects.get(user = u)
    grp = prof.groupname
    if page == 'pages':
        if grp != 'Admin' and grp != 'Author':
            return True
        return False
    else:
        if grp != 'Admin' and grp != 'Moderator':
            return True
        return False


def admin_messages(request, page):
    """Page with a list of received feedback."""
    if no_access(request, 'messages'):
        return HttpResponseRedirect(reverse('no_access'))
    grp = get_info(request)
    count = Message.objects.count()
    pages = int(count/10) + 1
    pg = int(page)
    if pg < 1 or pg > pages:
        raise Http404()
    else:
        if pg != pages:
            message_list = Message.objects.all()[(pg-1)*10:(pg-1)*10+10]
        else:
            message_list = Message.objects.all()[(pg-1)*10:count]
        template = loader.get_template('main/admin_messages.html')
        context = RequestContext(request, {
            'message_list':message_list,
            'pages':[i+1 for i in range(pages)],
            'selected_page':pg,
            'group':grp
        })
        return HttpResponse(template.render(context))

def admin_messages_sort(request, sort_by, order, page):
    """Page with feedback sorted."""
    if no_access(request, 'messages'):
        return HttpResponseRedirect(reverse('no_access'))
    if (sort_by != 'id' and sort_by != 'name' and sort_by != 'email' and sort_by != 'text' and sort_by != 'add_date' and sort_by != 'ip_address'):
        return HttpResponseRedirect(reverse('admin_messages_index'))
    if (order != 'asc' and order != 'desc'):
        return HttpResponseRedirect(reverse('admin_messages_index'))
    grp = get_info(request)
    ord = ''
    if order == 'desc':
        ord = '-'
    count = Message.objects.count()
    pages = int(count/10) + 1
    pg = int(page)
    if pg < 1 or pg > pages:
        raise Http404()
    else:
        if pg != pages:
            message_list = Message.objects.all().order_by(ord+sort_by)[(pg-1)*10:(pg-1)*10+10]
        else:
            message_list = Message.objects.all().order_by(ord+sort_by)[(pg-1)*10:count]
        template = loader.get_template('main/admin_messages.html')
        context = RequestContext(request, {
            'message_list':message_list,
            'pages':[i+1 for i in range(pages)],
            'selected_page':pg,
            'sort_by':sort_by,
            'order':order,
            'group':grp
        })
        return HttpResponse(template.render(context))

def admin_messages_index(request):
    """Redirect to first page with feedback."""
    return HttpResponseRedirect(reverse('admin_messages', args=(1,)))

def admin_pages(request):
    """Page with list of articles."""
    if get_info(request) == 'Moderator':
        return HttpResponseRedirect(reverse('admin_messages_index'))
    if no_access(request, 'pages'):
        return HttpResponseRedirect(reverse('no_access'))
    grp = get_info(request)
    pages = Page.objects.all()
    template = loader.get_template('main/admin_pages.html')
    context = RequestContext(request, {
        'pages':pages,
        'group':grp
    })
    return HttpResponse(template.render(context))

def change_status(request, page_order):
    """Change status of a page."""
    if no_access(request, 'pages'):
        return HttpResponseRedirect(reverse('no_access'))
    num = Page.objects.count()
    po = int(page_order)
    if po < 1 or len(Page.objects.filter(order=po)) == 0:
        return HttpResponseRedirect(reverse('admin_pages'))
    page = Page.objects.get(order = po)
    if page.status == 'hidden':
        page.status = 'published'
    else:
        page.status = 'hidden'
    page.save()
    return HttpResponseRedirect(reverse('admin_pages'))

def sort_pages(request, sort_by, order):
    """Page with list of articles sorted."""
    if no_access(request, 'pages'):
        return HttpResponseRedirect(reverse('no_access'))
    if (order != 'asc' and order != 'desc') or (sort_by != 'title' and sort_by != 'add_date' and sort_by != 'order' and sort_by != 'status' and sort_by != 'access' and sort_by != 'added_by'):
        return HttpResponseRedirect(reverse('admin_pages'))
    grp = get_info(request)
    ord = ''
    if order == 'desc':
        ord = '-'
    pages = Page.objects.order_by(ord+sort_by)
    template = loader.get_template('main/admin_pages.html')
    context = RequestContext(request, {
        'pages':pages,
        'group':grp
    })
    return HttpResponse(template.render(context))

def pages_del_selected(request):
    """Delete selected articles."""
    if no_access(request, 'pages'):
        return HttpResponseRedirect(reverse('no_access'))
    grp = get_info(request)
    error = ''
    pages = Page.objects.all()
    if request.method == "POST":
        try:
            checked = []
            for page in pages:
                if 'checkbox_' + str(page.order) in request.POST:
                    checked.append(page.order)
            print(checked)
            if len(checked) == 0:
                raise Exception('No pages selected.')
        except Exception as ex:
            error = ex
        else:
            if 'delete' in request.POST:
                for i in checked:
                    Page.objects.get(order=i).delete()
            elif 'submit' in request.POST:
                for i in checked:
                    p = Page.objects.get(order=i)
                    p.status = 'published'
                    p.save()
            elif 'change' in request.POST:
                for i in checked:
                    p = Page.objects.get(order=i)
                    p.access = request.POST['access']
                    p.save()
            return HttpResponseRedirect(reverse('admin_pages'))
    template = loader.get_template('main/admin_pages.html')
    context = RequestContext(request, {
        'pages':pages,
        'error_message':error,
        'group':grp
    })
    return HttpResponse(template.render(context))

def messages_form(request):
    """Choose between deleting and answering."""
    if no_access(request, 'messages'):
        return HttpResponseRedirect(reverse('no_access'))
    if request.method == "POST":
        if request.POST.get('del_selected'):
            return messages_del_selected(request)
        else:
            return messages_answer(request)

def messages_answer(request):
    """Answer the feedback."""
    if no_access(request, 'messages'):
        return HttpResponseRedirect(reverse('no_access'))
    if request.method == 'POST':
        num = Message.objects.count()
        max = Message.objects.order_by('-id')[0].id
        for i in range(max+1):
            if request.POST.get('answer_'+str(i)):
                id = i
                break
        message = Message.objects.get(id=id)
        message.answer = request.POST.get('answer_'+str(id)+'_text')
        message.save()
    return HttpResponseRedirect(reverse('admin_messages_index'))


def messages_del_selected(request):
    """Delete selected feedback."""
    if no_access(request, 'messages'):
        return HttpResponseRedirect(reverse('no_access'))
    error = ''
    count = Message.objects.count()
    pages = int(count/10) + 1
    messages = Message.objects.all()
    if request.method == "POST":
        try:
            checked = []
            for message in messages:
                if 'checkbox_' + str(message.id) in request.POST:
                    checked.append(message.id)
            if len(checked) == 0:
                raise Exception('No messages selected.')
        except Exception as ex:
            error = ex
        else:
            for i in checked:
                Message.objects.get(id=i).delete()
            return HttpResponseRedirect(reverse('admin_messages_index'))
    template = loader.get_template('main/admin_messages.html')
    context = RequestContext(request, {
        'message_list':messages[0:10],
        'pages':[i+1 for i in range(pages)],
        'selected_page':1,
        'error_message':error
    })
    return HttpResponse(template.render(context))

def pages_edit(request, page_order):
    """Page with a form for editing article."""
    if no_access(request, 'pages'):
        return HttpResponseRedirect(reverse('no_access'))
    grp = get_info(request)
    error = ''
    if request.method == 'POST':
        try:
            url = request.POST['url']
            title = request.POST['title']
            pic = request.POST['pic']
            order = int(request.POST['order'])
            order_old = int(request.POST['order_old'])
            access = request.POST['access']
            status = request.POST['status']
            text = request.POST['text']
            tags = request.POST['tags']
            taglist = [x.strip() for x in tags.split(',')]
            parags = []
            i = 1
            while 'section_title_'+str(i) in request.POST:
                parags.append({'title':request.POST['section_title_'+str(i)], 'text':request.POST['section_text_'+str(i)], 'order':i})
                i += 1
            if title == '':
                raise Exception('Enter page title.')
            if order < 0:
                raise Exception('Order must be a positive number.')
            if len(Page.objects.filter(order=order)) > 0 and order != order_old:
                raise Exception('Order number must be unique')
            for par in parags:
                if par['title'] == '':
                    raise Exception('Sections must have titles')
        except Exception as ex:
            error = ex
        else:
            pag = Page.objects.get(url=url)
            pag.title = title
            pag.pic = pic
            pag.order = order
            pag.access = access
            pag.status = status
            pag.text = text
            Paragraph.objects.filter(page=pag).delete()
            pag.tags.clear()
            for tag in taglist:
                if len(Tag.objects.filter(name=tag)) == 1:
                    pag.tags.add(Tag.objects.get(name=tag))
                else:
                    tg = Tag(name=tag)
                    tg.save()
                    pag.tags.add(tg)
            pag.save()
            for parag in parags:
                paragraph = Paragraph(title=parag['title'], text=parag['text'], order=parag['order'], page=pag)
                paragraph.save()
            return HttpResponseRedirect(reverse('admin_pages'))
    if len(Page.objects.filter(order=page_order)) == 0:
        return HttpResponseRedirect(reverse('admin_pages'))
    page = Page.objects.get(order=page_order)
    strtgs = ''
    tgs = page.tags.all()
    for tag in tgs:
        strtgs += tag.name + ', '
    if strtgs != '':
        strtgs = strtgs[:-2]
    p = {'url':page.url, 'title':page.title, 'text':page.text, 'pic':page.pic, 'date':page.add_date, 'paragraphs':[], 'access':page.access, 'status':page.status, 'order':page.order, 'tags':strtgs}
    pars = Paragraph.objects.filter(page=page).order_by('order')
    for par in pars:
        p['paragraphs'].append({'title':par.title, 'text':par.text, 'order':par.order})
    template = loader.get_template('main/admin_edit_page.html')
    context = RequestContext(request, {
        'page':p,
        'error_message':error,
        'edit':'yes',
        'group':grp
    })
    return HttpResponse(template.render(context))

def add_page(request):
    """Page with a form for creating an article."""
    if no_access(request, 'pages'):
        return HttpResponseRedirect(reverse('no_access'))
    grp = get_info(request)
    error = ''
    p = {'url':'', 'title':'', 'text':'', 'pic':'', 'date':'', 'paragraphs':[], 'access':'', 'status':'', 'order':'', 'tags':''}
    if request.method == 'POST':
        try:
            url = request.POST['url']
            title = request.POST['title']
            pic = request.POST['pic']
            order = int(request.POST['order'])
            access = request.POST['access']
            status = request.POST['status']
            text = request.POST['text']
            tags = request.POST['tags']
            p['url'] = url
            p['title'] = title
            p['text'] = text
            p['pic'] = pic
            p['access'] = access
            p['status'] = status
            p['order'] = order
            p['tags'] = tags
            parags = []
            taglist = [x.strip() for x in tags.split(',')]
            i = 1
            while 'section_title_'+str(i) in request.POST:
                parags.append({'title':request.POST['section_title_'+str(i)], 'text':request.POST['section_text_'+str(i)], 'order':i})
                i += 1
            p['paragraphs'] = parags
            if title == '':
                raise Exception('Enter page title.')
            if url == '':
                raise Exception('Enter page URL')
            if order < 0:
                raise Exception('Order must be a positive number.')
            if len(Page.objects.filter(order=order)) > 0:
                raise Exception('Order number must be unique')
            for par in parags:
                if par['title'] == '':
                    raise Exception('Sections must have titles')
        except Exception as ex:
            error = ex
        else:
            pag = Page(title=title, url=url, pic=pic, order=order, access=access, status=status, text=text, add_date=datetime.now().date(), added_by=request.user.username)
            pag.save()
            for tag in taglist:
                if len(Tag.objects.filter(name=tag)) == 1:
                    pag.tags.add(Tag.objects.get(name=tag))
                else:
                    tg = Tag(name=tag)
                    tg.save()
                    pag.tags.add(tg)
            pag.save()
            for parag in parags:
                paragraph = Paragraph(title=parag['title'], text=parag['text'], order=parag['order'], page=pag)
                paragraph.save()
            
            return HttpResponseRedirect(reverse('admin_pages'))
    template = loader.get_template('main/admin_edit_page.html')
    context = RequestContext(request, {
        'page':p,
        'error_message':error,
        'edit':'no',
        'group':grp
    })
    return HttpResponse(template.render(context))

def pages_delete(request, page_order):
    """Delete an article."""
    if no_access(request, 'pages'):
        return HttpResponseRedirect(reverse('no_access'))
    Page.objects.get(order=page_order).delete()
    return HttpResponseRedirect(reverse('admin_pages'))

def admin_questions(request):
    """Page with a list of polls."""
    if no_access(request, 'questions'):
        return HttpResponseRedirect(reverse('no_access'))
    grp = get_info(request)
    questions = []
    qs = Question.objects.all()
    for question in qs:
        answers = Answer.objects.filter(question=question)
        ans = []
        for answer in answers:
            ans.append({'text':answer.text, 'votes_count':answer.votes_count})
        questions.append({'name': question.name, 'id':question.id, 'answers':ans})
    template = loader.get_template('main/admin_questions.html')
    context = RequestContext(request, {
        'questions':questions,
        'group':grp
    })
    return HttpResponse(template.render(context))

def add_question(request):
    """Page for adding a poll."""
    if no_access(request, 'questions'):
        return HttpResponseRedirect(reverse('no_access'))
    grp = get_info(request)
    error = ''
    q = {'name':'', 'text':''}
    if request.method == 'POST':
        try:
            name = request.POST['name']
            text = request.POST['text']
            q['name'] = name
            q['text'] = text
            answer_count = int(request.POST['answer_count'])
            answers = [request.POST[('ans'+str(i+1))] for i in range(answer_count)]
            if name == '':
                raise Exception('Enter caption.')
            if text == '':
                raise Exception('Enter question text.')
            for answer in answers:
                if answer == '':
                    raise Exception('Enter all answers')
        except Exception as ex:
            error = ex
        else:
            question = Question(name=name, text=text, answer_count=answer_count)
            question.save()
            for answer in answers:
                ans = Answer(text=answer, votes_count=0, question=question)
                ans.save()
            return HttpResponseRedirect(reverse('admin_questions'))
    template = loader.get_template('main/admin_add_question.html')
    context = RequestContext(request, {
        'question':q,
        'error_message':error,
        'group':grp
    })
    return HttpResponse(template.render(context))

def del_question(request, id):
    """Page for deleting a poll."""
    if no_access(request, 'questions'):
        return HttpResponseRedirect(reverse('no_access'))
    if len(Question.objects.filter(id=id)) == 0:
        return HttpResponseRedirect(reverse('admin_questions'))
    q = Question.objects.get(id=id)
    q.delete()
    return HttpResponseRedirect(reverse('admin_questions'))