"""Small helpers used everywhere: log_activity(), paginate(), querystring()."""
from django.core.paginator import Paginator

from .models import ActivityLog


def get_client_ip(request):
    """Best-effort visitor IP address for the audit log."""
    if request is None:
        return None
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")


def log_activity(user, action, description, request=None):
    """Write one row to the audit log."""
    return ActivityLog.objects.create(
        user=user if (user is not None and user.is_authenticated) else None,
        action=action,
        description=description[:255],
        ip_address=get_client_ip(request) or None,
    )


def paginate(request, queryset, per_page=10):
    """Split a queryset into pages. Returns (page_obj, page_range) for the pagination partial."""
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(request.GET.get("page"))
    page_range = list(paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1))
    return page_obj, page_range


def querystring(request, exclude=("page",)):
    """Current URL parameters without "page" so filters survive when changing pages."""
    params = request.GET.copy()
    for key in exclude:
        params.pop(key, None)
    return params.urlencode()
