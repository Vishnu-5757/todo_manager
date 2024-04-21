
from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from datetime import date,datetime
from django.db.models import Max
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Avg
from django.template.loader import get_template
from datetime import datetime, timedelta
from django.db.models import Count
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .utilities.gist import export_project_summary_as_gist

from .forms import CreateUserForms
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



def register(request):
   if request.user.is_authenticated:
      return redirect('home')
   else:
    form=CreateUserForms
    context={
        'form':form
    }
    if request.method == "POST":
        form=CreateUserForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'user/user_register.html',context)



def loginPage(request):
    if request.user.is_authenticated:
      return redirect('home')
    else:  

     if request.method == "POST":
      username =  request.POST.get('username')
      password =  request.POST.get('password')

      user=authenticate(request,   username=username,    password=password)

      if user is not None:
         request.session['username'] = username
         login(request,user)

         return redirect('home')
      else:
         messages.info(request,'Username Or Password Is Incorrect')
         

     
    return render(request,'user/user_login.html')



@login_required(login_url='login')
def home(request):
    if request.method == 'POST' and 'create_project_btn' in request.POST:
        project_name = request.POST.get('projectName')
        user = request.user
        project = Project(title=project_name, uid=user)
        project.save()
        return HttpResponse('<script>alert("Created Successfully");window.location.href="/home"</script>')

        return redirect('home')
    username = request.session.get('username')

    projects = Project.objects.filter(uid=request.user)
    if username:
        print("Logged in username from session:", username)  # Print the username
        return render(request, 'user/user_home.html', {'username': username,'projects': projects})
            
    else:
        return redirect('login')
    
@csrf_exempt
def update_project_name(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))  # Parse request body JSON data
        project_id = data.get('id')
        new_name = data.get('name')

        try:
            project = Project.objects.get(pk=project_id)
            project.title = new_name
            project.save()
            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


    
@login_required
def my_project(request, project_id):  # Add project_id parameter here
    user = request.user
    project = get_object_or_404(Project, pk=project_id, uid=user)
    todos = project.todos.all()
    pending_todos = project.todos.filter(status='pending')
    completed_todos = project.todos.filter(status='completed')
    
    context = {
        'project': project,
        'todos':todos,
        'pending_todos': pending_todos,
        'completed_todos': completed_todos,
    }

    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            todo = Todo.objects.create(description=description, project=project, uid=user)
            messages.success(request, 'Todo created successfully.')
            return redirect('my_project', project_id=project_id)  
        else:
           
            pass

    return render(request, 'user/my_project.html', context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    # Delete associated todos
    project.todos.all().delete()
    
    # Delete the project
    project.delete()
    return HttpResponse('<script>alert("Deleted");window.location.href="/home"</script>')

    
    return redirect('home')


def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        new_description = request.POST.get('description')
        if new_description:
            # Update description and updated_date
            todo.description = new_description
            todo.created_date = timezone.now()
            todo.save()
            return JsonResponse({'message': 'Todo updated successfully'})
        else:
            return JsonResponse({'error': 'Description is required'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    project_id = todo.project_id
    todo.delete()
    # messages.success(request, 'Todo deleted successfully.')
    
    delete_message = f' "{todo.description}" deleted successfully.'
    messages.info(request, delete_message)
    
    return redirect('my_project', project_id=project_id)




@login_required
def update_todo_status(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    project_id = todo.project_id
    if request.method == 'POST':
        # Toggle the status
        if todo.status == 'pending':
            todo.status = 'completed'
        else:
            todo.status = 'pending'
        todo.save()
    return redirect('my_project', project_id=project_id)

@login_required
def export_as_gist(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id, uid=user)
    todos = project.todos.all()
    export_project_summary_as_gist(project.title,todos)

    print(todos)
    return redirect('my_project', project_id=project_id)



def LogoutPage(request):
   logout(request)
   return redirect('login')

