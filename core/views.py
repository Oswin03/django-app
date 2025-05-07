from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import AndroidApp, Task
from .serializers import AndroidAppSerializer, TaskSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import Task



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

class AndroidAppViewSet(viewsets.ModelViewSet):
    queryset = AndroidApp.objects.all()
    serializer_class = AndroidAppSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([AllowAny])
def upload_page(request):
    return render(request, 'upload.html')

# Example: in your TaskSerializer's create method
def create(self, validated_data):
    task = super().create(validated_data)
    task.user.points += 10  # or any logic you want
    task.user.save()
    return task

@login_required
def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})


@login_required
def admin_tasks(request):
    tasks = Task.objects.select_related('user', 'app')

    user_filter = request.GET.get("user")
    app_filter = request.GET.get("app")
    status_filter = request.GET.get("status")

    if user_filter:
        tasks = tasks.filter(user__id=user_filter)
    if app_filter:
        tasks = tasks.filter(app__id=app_filter)
    if status_filter == "completed":
        tasks = tasks.filter(completed=True)
    elif status_filter == "pending":
        tasks = tasks.filter(completed=False)

    return render(request, "admin/tasks.html", {"tasks": tasks})


@login_required
def mark_task_completed(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
    except Task.DoesNotExist:
        pass
    return redirect('admin_tasks')

# Create your views here.
