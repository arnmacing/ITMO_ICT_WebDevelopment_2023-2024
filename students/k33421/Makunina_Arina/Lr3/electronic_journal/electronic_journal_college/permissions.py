from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'student'


class IsHeadmaster(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'headmaster'
