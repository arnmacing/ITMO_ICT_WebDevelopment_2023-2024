from rest_framework import viewsets
from .permissions import IsTeacher, IsStudent
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import JsonResponse


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


class DisciplineViewSet(viewsets.ModelViewSet):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class TeachingAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TeachingAssignment.objects.all()
    serializer_class = TeachingAssignmentSerializer
    permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsStudent]


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher]


from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = request.user
            role = user.groups.first().name if user.groups.exists() else None
            data = {'token': response.data['token'], 'role': role}
            return Response(data)
        return response


def get_user_group(user):
    return user.groups.first().name if user.groups.exists() else None


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = request.user
            role = get_user_group(user)
            data = {'token': response.data['token'], 'role': role}
            return Response(data)
        return response


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if a token already exists
            token, created = Token.objects.get_or_create(user=user)

            return JsonResponse({'auth_token': token.key, 'role': get_user_group(user)})
        else:
            return JsonResponse({'error': 'Authentication failed'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
