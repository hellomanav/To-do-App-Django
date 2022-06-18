from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import os,random
from pathlib import Path
from django.templatetags.static import static
from django.contrib.staticfiles.finders import find
from django.conf import settings
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage

def index(request):
    s = StaticFilesStorage()
    print('static path is')
    print(s.location)
    # print(dir(s))
    # print('static root is')
    # print(settings.STATIC_ROOT)
   
    # get random image to display on home page
    img_list=[]
    try:
        # get static paths of production server
        # img_dir=os.path.join(s.location,"tasks","images")
        # img_list=list(get_files(s, location=os.path.join('tasks','images')))
        img_dir=os.path.join(settings.STATIC_ROOT,"tasks","images")
        img_list=os.listdir(img_dir)
    except Exception as ex:
        print('production static location not found')
        print('exception trace ---',str(ex))
        try:
            # get static paths of development server
            # img_dir=os.path.normpath(static('tasks/images'))[1:]
            img_dir=os.path.join("static","tasks","images")
            img_list=os.listdir(img_dir)
        except Exception as e:
            print('no directory found for task images')
            print('exception trace ---',str(e))
    
    img_name=''
    try:
        img_name=str(random.choice(img_list))
    except Exception as e:
        print(str(e))

    # get list of all tasks to display on page
    tasks = Task.objects.all()
    form = TaskForm()

    # create new task and redirect to home/list page
    if request.method =='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'tasks':tasks, 'form':form,'img_url':img_name}
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