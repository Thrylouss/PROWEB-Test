from datetime import date

from django.contrib.auth.models import User
from rest_framework import serializers

from todoApp.models import Task, Comment


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UsersTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TaskSerializer(serializers.ModelSerializer):
    user = UsersTasksSerializer(read_only=True)
    due_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_at', 'user', 'task',)
