from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import LostItem, FoundItem, ClaimRequest
from django.db.models import Count
from .forms import LostItemForm, FoundItemForm, ClaimRequestForm
from .matching import find_potential_matches

class LostItemListView(LoginRequiredMixin, ListView):
    model = LostItem
    template_name = 'lostfound/lost_list.html'
    context_object_name = 'lost_items'
    
    def get_queryset(self):
        queryset = LostItem.objects.all().order_by('-created_at')
        status_filter = self.request.GET.get('status', 'open')
        if status_filter in ('open', 'matched', 'closed'):
            queryset = queryset.filter(status=status_filter)
            
        my_reports = self.request.GET.get('my_reports', 'false')
        if my_reports == 'true':
            queryset = queryset.filter(reporter=self.request.user)
            
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(description__icontains=q)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = LostItem.objects.values('status').annotate(count=Count('id'))
        status_counts = {c['status']: c['count'] for c in counts}
        context['status_counts'] = status_counts
        return context

class LostItemDetailView(LoginRequiredMixin, DetailView):
    model = LostItem
    template_name = 'lostfound/lost_detail.html'
    context_object_name = 'lost_item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.object.reporter or self.request.user.role in ('staff', 'admin') or self.request.user.is_superuser:
            context['potential_matches'] = find_potential_matches(self.object)[:5]
        return context

class LostItemCreateView(LoginRequiredMixin, CreateView):
    model = LostItem
    form_class = LostItemForm
    template_name = 'lostfound/lost_form.html'
    success_url = reverse_lazy('lostfound:lost_list')
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        messages.success(self.request, "Lost item reported successfully!")
        return super().form_valid(form)

class LostItemUpdateView(LoginRequiredMixin, UpdateView):
    model = LostItem
    form_class = LostItemForm
    template_name = 'lostfound/lost_form.html'
    
    def get_queryset(self):
        return LostItem.objects.filter(reporter=self.request.user)
        
    def form_valid(self, form):
        messages.success(self.request, "Report updated successfully!")
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('lostfound:lost_detail', kwargs={'pk': self.object.pk})

class FoundItemListView(LoginRequiredMixin, ListView):
    model = FoundItem
    template_name = 'lostfound/found_list.html'
    context_object_name = 'found_items'
    
    def get_queryset(self):
        queryset = FoundItem.objects.all().order_by('-created_at')
        status_filter = self.request.GET.get('status', 'unclaimed')
        if status_filter in ('unclaimed', 'claimed'):
            queryset = queryset.filter(status=status_filter)
            
        my_reports = self.request.GET.get('my_reports', 'false')
        if my_reports == 'true':
            queryset = queryset.filter(finder=self.request.user)
            
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(description__icontains=q)
            
        return queryset

class FoundItemDetailView(LoginRequiredMixin, DetailView):
    model = FoundItem
    template_name = 'lostfound/found_detail.html'
    context_object_name = 'found_item'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_claim'] = ClaimRequest.objects.filter(
            found_item=self.object,
            claimant=self.request.user
        ).first()
        
        if self.request.user == self.object.finder or self.request.user.role in ('staff', 'admin') or self.request.user.is_superuser:
            context['claim_requests'] = self.object.claim_requests.all().order_by('-created_at')
            
        context['claim_form'] = ClaimRequestForm()
        return context

class FoundItemCreateView(LoginRequiredMixin, CreateView):
    model = FoundItem
    form_class = FoundItemForm
    template_name = 'lostfound/found_form.html'
    success_url = reverse_lazy('lostfound:found_list')
    
    def form_valid(self, form):
        form.instance.finder = self.request.user
        messages.success(self.request, "Found item reported successfully!")
        return super().form_valid(form)

class ClaimRequestCreateView(LoginRequiredMixin, CreateView):
    model = ClaimRequest
    form_class = ClaimRequestForm
    
    def post(self, request, *args, **kwargs):
        found_item = get_object_or_404(FoundItem, pk=self.kwargs['found_item_pk'])
        if found_item.finder == request.user:
            messages.error(request, "You cannot submit a claim for an item you found yourself!")
            return redirect('lostfound:found_detail', pk=found_item.pk)
            
        if found_item.status == 'claimed':
            messages.error(request, "This item has already been claimed.")
            return redirect('lostfound:found_detail', pk=found_item.pk)
            
        existing = ClaimRequest.objects.filter(found_item=found_item, claimant=request.user).first()
        if existing:
            messages.warning(request, "You have already submitted a claim for this item.")
            return redirect('lostfound:found_detail', pk=found_item.pk)
            
        form = ClaimRequestForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.found_item = found_item
            claim.claimant = request.user
            claim.save()
            messages.success(request, "Your claim request has been submitted successfully!")
        return redirect('lostfound:found_detail', pk=found_item.pk)

class ClaimRequestActionView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        claim = get_object_or_404(ClaimRequest, pk=pk)
        action = request.POST.get('action')
        
        is_authorized = (
            request.user == claim.found_item.finder or 
            request.user.role in ('staff', 'admin') or 
            request.user.is_superuser
        )
        if not is_authorized:
            raise PermissionDenied("You are not authorized to manage this claim.")
            
        if action == 'approve':
            claim.status = 'approved'
            claim.save()
            
            found_item = claim.found_item
            found_item.status = 'claimed'
            found_item.save()
            
            other_claims = found_item.claim_requests.filter(status='pending').exclude(pk=claim.pk)
            for other in other_claims:
                other.status = 'rejected'
                other.save()
                
            messages.success(request, f"Claim request for '{found_item.title}' approved successfully!")
        elif action == 'reject':
            claim.status = 'rejected'
            claim.save()
            messages.info(request, "Claim request has been rejected.")
            
        return redirect('lostfound:found_detail', pk=claim.found_item.pk)
