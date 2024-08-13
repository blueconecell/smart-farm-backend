from django.contrib import admin
from .models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_members', 'created_at')

    def get_members(self, obj):
        return ", ".join([member.username for member in obj.members.all()])

    get_members.short_description = 'Members'

admin.site.register(Team, TeamAdmin)