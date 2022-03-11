from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError

from markdown2 import Markdown
from datetime import datetime

from .models import *
from .forms import *

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "notes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "notes/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "notes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "notes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "notes/register.html")


def error_404(request, exception):
    return render(request, 'notes/error_404.html')


def index(request):
    return render(request, 'notes/index.html', {
        'notes': Note.objects.all(),
        'todolists': TodoList.objects.all(),
        'tags': Tag.objects.all(),
    })


def note(request, note_id):
    note = Note.objects.get(pk=note_id)
    if note:
        markdown = Markdown()
        return render(request, 'notes/note.html', {
            'note': note,
            'content': markdown.convert(note.content)
        })
    else:
        return render(request, 'notes/error_404.html')


def new_note(request):
    if request.method == 'POST':

            title = request.POST.get('title')
            content = request.POST.get('content')

            note = Note.objects.create(title=title, content=content, creation_date=datetime.now(), user=request.user)

            note.save()

            return HttpResponseRedirect(reverse('note', args=[note.id]))

    else:
        return render(request, 'notes/new_note.html')


def edit_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        note.title = title
        note.content = content

        note.save()

        # return redirect('/note/' + title)
        return HttpResponseRedirect(reverse('note', args=[note_id]))

    return render(request, 'notes/edit.html', {
        'note': note,
    })


def delete_note(request, note_id):
    Note.objects.get(pk=note_id).delete()

    return HttpResponseRedirect(reverse('index'))


def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        results = []

        for note in Note.objects.all():
            if query.lower() in note.title.lower() or query.lower() == note.title.lower():
                results.append(note)

        return render(request, 'notes/search.html', {
            'results': results
        })

    else:
        return HttpResponseRedirect(reverse('index'))


def new_todolist(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        todolist = TodoList.objects.create(title=title, user=request.user)
        todolist.save()

        return HttpResponseRedirect(reverse('todolist', args=[todolist.id]))

    else:
        return render(request, 'notes/new_todolist.html')


def todolist(request, list_id):
    todolist = TodoList.objects.get(pk=list_id)
    tasks = todolist.tasks

    # true if there are any completed tasks in the todolist, false otherwise
    completed_tasks = False
    for task in tasks.all():
        if task.completed:
            completed_tasks = True
    return render(request, 'notes/todolist.html', {
        'todolist': todolist,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
    })


def add_task(request, list_id):
    todolist = TodoList.objects.get(pk=list_id)

    if request.method == 'POST':
        text = request.POST.get('text')

        task = Task.objects.create(text=text, todolist=todolist)
        task.save()

        return HttpResponseRedirect(reverse('todolist', args=[todolist.id]))

    else:
        return HttpResponseRedirect(reverse('todolist', args=[todolist.id]))


def complete_task(request, task_id):
    task = Task.objects.get(pk=task_id)

    if task.completed:
        task.completed = False
    else:
        task.completed = True

    task.save()

    return HttpResponseRedirect(reverse('todolist', args=[task.todolist.id]))


def clear_completed(request, todolist_id):
    todolist = TodoList.objects.get(pk=todolist_id)

    for task in todolist.tasks.all():
        if task.completed:
            task.delete()

    return HttpResponseRedirect(reverse('todolist', args=[todolist.id]))


def delete_todolist(request, todolist_id):
    TodoList.objects.get(pk=todolist_id).delete()

    return HttpResponseRedirect(reverse('index'))


def tag_view(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    return render(request, 'notes/tag.html', {
        'tag': tag,
    })


def new_tag(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        tag = Tag.objects.create(name=name, user=request.user)
        tag.save()

        return HttpResponseRedirect(reverse('tag', args=[tag.id]))

    else:
        return render(request, 'notes/new_tag.html')


def edit_tags(request, note_id):
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        tags = request.POST.getlist('tags')
        for tag in tags:
            tag_object = Tag.objects.get(pk=tag)
            if note not in tag_object.notes.all():
                tag_object.notes.add(note)
            else:
                tag_object.notes.remove(note)


        return HttpResponseRedirect(reverse('note', args=[note.id]))
    else:
        return render(request, 'notes/note.html', {
            'tags': Tag.objects.all(),
            'note': note,
            'tag_form': True,
        })