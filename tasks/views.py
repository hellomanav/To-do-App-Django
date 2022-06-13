from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *
import os,random
from pathlib import Path
from django.templatetags.static import static
from django.conf import settings
from django.contrib.staticfiles.utils import get_files
from django.contrib.staticfiles.storage import StaticFilesStorage



def index(request):
    # print(request)
    # path = static('tasks/images')
    # print(path)
    s = StaticFilesStorage()
    print('sstatic path is')
    print(s.location)
    # print(dir(s))
    # print('static root is')
    # print(settings.STATIC_ROOT)
    # print('directories')

    # production? 
    # These both search in static root directory
    # s = StaticFilesStorage()
    # img_list=list(get_files(s, location=os.path.join('tasks','images')))
    # img_dir=os.path.join(settings.STATIC_ROOT,"tasks","images")
    # img_list=os.listdir(img_dir)

    # 111111111111111111111111111111111
    img_dir=os.path.join(s.location,"tasks","images")
    img_list=os.listdir(img_dir)
    # ````````````````````````````````
    
    img_name=''
    try:
        img_name=str(random.choice(img_list))
    except Exception as e:
        print(str(e))
    tasks = Task.objects.all()
    form = TaskForm()

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