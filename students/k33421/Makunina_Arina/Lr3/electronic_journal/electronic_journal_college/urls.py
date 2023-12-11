from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'disciplines', DisciplineViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'teaching_assignments', TeachingAssignmentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'timeslots', TimeSlotViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'grades', GradeViewSet)

# Настройка представлений drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for my app electronic_journal_college",
        terms_of_service="https://www.example.com/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),  # Для использования авторизации по токенам
    path('auth/', include('djoser.urls.jwt')),  # Для использования JWT
    # Документация Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
