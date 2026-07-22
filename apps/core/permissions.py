def is_staff_or_admin(user):
    return user.is_authenticated and (user.role in ('staff', 'admin') or user.is_superuser)

def is_owner_or_staff(user, obj):
    if not user.is_authenticated:
        return False
    if user.role in ('staff', 'admin') or user.is_superuser:
        return True
    
    for attr in ('reporter', 'submitter', 'claimant', 'finder', 'user'):
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            if val == user:
                return True
            
    return False
