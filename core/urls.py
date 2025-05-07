from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AndroidAppViewSet, TaskViewSet, RegisterView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from .views import upload_page
from . import views

router = DefaultRouter()
router.register('apps', AndroidAppViewSet)
router.register('tasks', TaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', upload_page, name='upload-page'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-tasks/", views.admin_tasks, name="admin_tasks"),
    path("admin-mark-task/<int:task_id>/", views.mark_task_completed, name="mark_task_completed"),
   
]
