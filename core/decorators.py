"""Role-based access control decorators."""
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from accounts.models import CustomUser

Role = CustomUser.Role


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not user.is_active or user.role not in roles:
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


super_admin_required = role_required(Role.SUPER_ADMIN)
admin_required = role_required(Role.ADMIN)
staff_required = role_required(Role.SUPER_ADMIN, Role.ADMIN)


def permission_flag_required(flag):
    """Fine-grained permission (e.g. 'may_archive_patients'). Use after staff_required."""
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not getattr(request.user, flag, False):
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
