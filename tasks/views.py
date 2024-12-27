from msilib.schema import ListView
from django.views.generic import DetailView

from tasks.models import Task, Category

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        search_query = self.reqest.GET.get('query')

        if category:
            queryset = queryset.filter(category__icontains=category)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class TasksDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'task'

