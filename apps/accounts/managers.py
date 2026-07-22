from django.contrib.auth.models import UserManager as BaseUserManager

class UserManager(BaseUserManager):
    def students(self):
        return self.filter(role='student')
        
    def staff(self):
        return self.filter(role='staff')
        
    def admins(self):
        return self.filter(role='admin')
