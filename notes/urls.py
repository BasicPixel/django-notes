from django.urls.conf import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    path('search', views.search, name='search'),

    path('new_note', views.new_note, name='new_note'),
    path('note/<int:note_id>', views.note, name='note'),
    path('delete_note/<int:note_id>', views.delete_note, name='delete'),
    path('edit_note/<int:note_id>', views.edit_note, name='edit'),

    path('new_todolist', views.new_todolist, name='new_todolist'),
    path('todolist/<int:list_id>', views.todolist, name='todolist'),
    path('add_task/<int:list_id>', views.add_task, name='add_task'),
    path('complete_task/<int:task_id>',
         views.complete_task, name='complete_task'),
    path('clear_completed/<int:todolist_id>',
         views.clear_completed, name='clear_completed'),
    path('delete_todolist/<int:todolist_id>',
         views.delete_todolist, name='delete_todolist'),

    path('new_tag', views.new_tag, name='new_tag'),
    path('tag/<int:tag_id>', views.tag_view, name='tag'),
    path('edit_tags/<int:note_id>', views.edit_tags, name='edit_tags'),
]
