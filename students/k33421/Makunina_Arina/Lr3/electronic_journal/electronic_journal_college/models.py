from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"Room {self.number}"


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    room = models.CharField(max_length=100, blank=True, null=True)
    disciplines = models.ManyToManyField('Discipline', through='TeachingAssignment')

    def __str__(self):
        return self.name


class Discipline(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TeachingAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])

    class Meta:
        unique_together = ('teacher', 'discipline', 'semester')

    def __str__(self):
        return f"{self.discipline} - {self.teacher} (Semester {self.semester})"


class Student(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    DAYS_OF_WEEK = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )

    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, validators=[MinValueValidator(1), MaxValueValidator(7)])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        day_display = self.get_day_of_week_display()
        start_time_str = self.start_time.strftime('%H:%M')
        end_time_str = self.end_time.strftime('%H:%M')
        return f"{day_display} {start_time_str} - {end_time_str}"


class Schedule(models.Model):
    group = models.ForeignKey(Group, related_name='schedules', on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='schedules', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.name} {self.timeslot.get_day_of_week_display()} {self.timeslot.start_time} - " \
               f"{self.timeslot.end_time}, Room: {self.room.number} - {self.discipline.name} by {self.teacher.name}"


class Grade(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='grades', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='grades', on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=3, decimal_places=1,
                                validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])

    class Meta:
        unique_together = ('schedule', 'student')

    def __str__(self):
        return f"{self.student.name} - {self.schedule.discipline.name} - Grade: {self.grade}"


from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('headmaster', 'Headmaster'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Override the groups and user_permissions fields to set a custom related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_groups',  # Set a custom related_name
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_user_permissions',  # Set a custom related_name
        related_query_name='customuser',
    )

    class Meta:
        permissions = (("can_edit_schedule", "Can edit schedule"),)
