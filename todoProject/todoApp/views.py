from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from todoApp.models import Task, Comment
from todoApp.permissions import IsOwner
from todoApp.serializers import TaskSerializer, UserRegisterSerializer, CommentSerializer


# Create your views here.
class RegisterView(ListCreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class TaskAPIView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def get_queryset(self):
    #     return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class TasksByStatus(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        task_due_date = self.request.query_params.get('due_date')
        task_status = self.request.query_params.get('status')

        if task_status:
            queryset = queryset.filter(status=task_status)

        if task_due_date:
            print('true')
            queryset = queryset.all().order_by('due_date')

        return queryset


class TaskComments(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        task_id = self.request.data.get('task')

        queryset = Comment.objects.filter(task=task_id)
        if task_id:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        task_id = self.request.data.get('task')
        print(task_id)
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                raise serializers.ValidationError('Task does not exist')

            serializer.save(task=task)
        else:
            raise serializers.ValidationError('Task ID is required')
