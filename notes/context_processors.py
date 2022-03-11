from .models import *

def data(request):
    return {
        'notes': Note.objects.all(),
        'todolists': TodoList.objects.all(),
        'tags': Tag.objects.all(),
    }