from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *
import os,random
from pathlib import Path
from django.templatetags.static import static
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage



def index(request):
    print(request)
    # path = static('tasks/images')
    # print(path)
    s = StaticFilesStorage()
    img_list=list(get_files(s, location=os.path.join('tasks','images')))
    image_url=''
    try:
        image_url = random.choice(img_list).split('\\')[2]
    except Exception as e:
        print(str(e))
    print(image_url)
    print(type(image_url))
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method =='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'tasks':tasks, 'form':form,'image_url':image_url}
    return render(request, 'tasks/list.html', context)

def updateTask(request, pk):
	task = Task.objects.get(id=pk)

	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}

	return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    item.delete()
    return redirect('/')