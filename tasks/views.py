from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Category
from tasks.forms import TaskForm


def main_view(request):
    if request.method == 'GET':
        return render(request, "base.html")

def tasks_list_view(request):
    if request.method == 'GET':
        limit = 5
        page = int(request.GET.get('page', 1))
        search = request.GET.get('search')
        category = request.GET.get('category')
        ordering = request.GET.get('ordering')
        tasks = Task.objects.all()

        if search:
            tasks = tasks.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if category:
            tasks = tasks.filter(category_id=category)
        if ordering:
            tasks = tasks.order_by(ordering)

        max_pages = tasks.count() / limit
        if round(max_pages) < max_pages:
            max_pages = round(max_pages) + 1
        else:
            max_pages = round(max_pages)

        start = (page - 1) * limit
        end = start + limit
        tasks = tasks[start:end]
        categories = Category.objects.all()

        context = {
            "tasks": tasks,
            "categories": categories,
            "max_pages": range(1, max_pages + 1),
        }
        return render(request, "tasks/task_list.html", context=context)


def task_details_view(request, task_id):
    if request.method == 'GET':
        task = Task.objects.get(id=task_id)
        return render(request, "tasks/task_detail.html", context={"task": task})


def task_create_view(request):
    if request.method == 'GET':
        form = TaskForm()
        categories = Category.objects.all()
        return render(request, "tasks/task_create.html", context={"form": form, "categories": categories})

    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/tasks")
        categories = Category.objects.all()
        return render(request, "tasks/task_create.html", context={"form": form, "categories": categories})
