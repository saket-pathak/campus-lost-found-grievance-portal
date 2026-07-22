from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError

from .models import Grievance, StatusLog, GrievanceCategory
from .forms import GrievanceForm, GrievanceAssignForm, GrievanceStatusTransitionForm
from .workflow import transition_status

class GrievanceListView(LoginRequiredMixin, ListView):
    model = Grievance
    template_name = 'grievance/grievance_list.html'
    context_object_name = 'grievances'
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ('staff', 'admin') or user.is_superuser:
            queryset = Grievance.objects.all().order_by('-created_at')
            assigned = self.request.GET.get('assigned', '')
            if assigned == 'me':
                queryset = queryset.filter(assigned_to=user)
            elif assigned == 'unassigned':
                queryset = queryset.filter(assigned_to__isnull=True)
        else:
            queryset = Grievance.objects.filter(submitter=user).order_by('-created_at')
            
        status_filter = self.request.GET.get('status', '')
        if status_filter in ('open', 'in_review', 'resolved', 'escalated'):
            queryset = queryset.filter(status=status_filter)
            
        return queryset

class GrievanceDetailView(LoginRequiredMixin, DetailView):
    model = Grievance
    template_name = 'grievance/grievance_detail.html'
    context_object_name = 'grievance'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user.role == 'student' and not user.is_superuser:
            if obj.submitter != user:
                raise PermissionDenied("You are not authorized to view this grievance.")
        return obj
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['status_logs'] = self.object.status_logs.all().order_by('-timestamp')
        
        if user.role in ('staff', 'admin') or user.is_superuser:
            context['assign_form'] = GrievanceAssignForm(instance=self.object)
            context['status_form'] = GrievanceStatusTransitionForm(initial={'status': self.object.status})
        elif user == self.object.submitter:
            context['status_form'] = GrievanceStatusTransitionForm(initial={'status': self.object.status})
            
        return context

class GrievanceCreateView(LoginRequiredMixin, CreateView):
    model = Grievance
    form_class = GrievanceForm
    template_name = 'grievance/grievance_form.html'
    success_url = reverse_lazy('grievance:grievance_list')
    
    def form_valid(self, form):
        form.instance.submitter = self.request.user
        messages.success(self.request, "Grievance submitted successfully!")
        return super().form_valid(form)

class GrievanceAssignView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        grievance = get_object_or_404(Grievance, pk=pk)
        if not (request.user.role in ('staff', 'admin') or request.user.is_superuser):
            raise PermissionDenied("You are not authorized to assign handlers.")
            
        form = GrievanceAssignForm(request.POST, instance=grievance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Grievance assigned to {grievance.assigned_to.username} successfully.")
        else:
            messages.error(request, "Failed to assign handler.")
        return redirect('grievance:grievance_detail', pk=grievance.pk)

class GrievanceStatusTransitionView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        grievance = get_object_or_404(Grievance, pk=pk)
        form = GrievanceStatusTransitionForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            note = form.cleaned_data['note']
            try:
                transition_status(grievance, new_status, request.user, note)
                messages.success(request, f"Grievance status updated to {new_status} successfully.")
            except ValidationError as e:
                messages.error(request, f"Error: {e.message}")
        else:
            messages.error(request, "Failed to update status. Please check input.")
        return redirect('grievance:grievance_detail', pk=grievance.pk)
