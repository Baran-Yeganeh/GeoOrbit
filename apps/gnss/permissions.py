from rest_framework.permissions import BasePermission, SAFE_METHODS

class MissionPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        if request.method == 'POST':
            request_method_post = user.groups.filter(
                name__in = ['Employees', 'Managers']
                ).exists()
            return request_method_post

        if request.method in ['PUT','PATCH','DELETE']:
            manager_only = user.groups.filter(
                name__in = ['Managers']
            ).exists()
            return manager_only
        return False
