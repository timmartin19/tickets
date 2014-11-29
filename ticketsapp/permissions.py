__author__ = 'Tim Martin'
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.method in SAFE_METHODS


class TicketPermission(BasePermission):
    def has_object_permission(self, request, view, ticket):
        if request.user.is_superuser:
            return True
        elif request.method in SAFE_METHODS:
            return True
        elif request.user == ticket.client or request.user == ticket.consultant:
            return True
        return False