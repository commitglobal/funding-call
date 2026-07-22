from auditlog.middleware import AuditlogMiddleware
from django.http import HttpRequest


def get_remote_addr(request: HttpRequest):
    return AuditlogMiddleware._get_remote_addr(request)
