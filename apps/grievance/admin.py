from django.contrib import admin
from .models import GrievanceCategory, Grievance, StatusLog

@admin.register(GrievanceCategory)
class GrievanceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'created_at')
    search_fields = ('name', 'department')

@admin.register(Grievance)
class GrievanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'submitter', 'category', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'submitter__username', 'assigned_to__username')

@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('grievance', 'old_status', 'new_status', 'changed_by', 'timestamp')
    list_filter = ('old_status', 'new_status', 'timestamp')
    search_fields = ('grievance__title', 'changed_by__username', 'note')
