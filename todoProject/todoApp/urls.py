from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from todoApp.views import RegisterView, TaskAPIView, TaskDetailAPIView, TasksByStatus, TaskComments

schema_view = get_schema_view(
    openapi.Info(
        title="TODO API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenObtainPairView.as_view(), name='token_refresh'),

    path('users/', RegisterView.as_view(), name='user_register'),

    path('task/', TaskAPIView.as_view(), name='task'),
    path('task/<int:pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
    path('task/filter-by/', TasksByStatus.as_view(), name='task_filter_by_status'),
    path('task/comments/', TaskComments.as_view(), name='task_comments'),
]