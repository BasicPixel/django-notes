# Generated by Django 3.2.4 on 2021-07-06 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_alter_task_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='todo_list',
            new_name='todolist',
        ),
        migrations.AlterField(
            model_name='todolist',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todolists', to=settings.AUTH_USER_MODEL),
        ),
    ]