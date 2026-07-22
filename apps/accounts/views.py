from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserRegisterForm, UserProfileForm

User = get_user_model()

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    
    def get_success_url(self):
        return reverse('accounts:register_success') + f"?username={self.object.username}&email={self.object.email}&role={self.object.role}"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"Welcome to the Campus Portal, {self.object.username}!")
        return response

class RegisterSuccessView(TemplateView):
    template_name = 'accounts/register_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.GET.get('username', '')
        context['email'] = self.request.GET.get('email', '')
        context['role'] = self.request.GET.get('role', '')
        return context

class LoginView(BaseLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return reverse_lazy('core:home')

class LogoutView(BaseLogoutView):
    def get_default_redirect_url(self):
        return reverse_lazy('accounts:login')
        
    def dispatch(self, request, *args, **kwargs):
        if request.method in ('POST', 'GET'):
            messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
        
    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)
