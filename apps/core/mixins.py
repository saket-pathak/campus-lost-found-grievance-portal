from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []
    
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.role == 'admin' or user.is_superuser:
            return True
        return user.role in self.allowed_roles

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("You do not have permission to access this page.")
        return super().handle_no_permission()

class StaffOrAdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['staff', 'admin']
