from django.contrib import admin
from .models import Team, Racer, Race, RaceEntry, Comment


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'description', 'experience')
    list_filter = ('team', 'experience')


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'winner')
    list_filter = ('winner',)


@admin.register(RaceEntry)
class RaceEntryAdmin(admin.ModelAdmin):
    list_display = ('racer', 'race')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'race', 'comment_type', 'created_at', 'rating')
    list_filter = ('comment_type', 'created_at')