from django import forms
from django.forms import ModelForm

from notes import models

class NoteForm(ModelForm):
    class Meta:
        model = models.Note
        fields = ['title', 'content']