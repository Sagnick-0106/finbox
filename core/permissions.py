from rest_framework.permissions import BasePermission


class MatchUserIdPermission(BasePermission):
    def has_permission(self, request, view):
        user_id_from_data = (request.data.get('User_ID') if request.data.get('User_ID')
                             else request.resolver_match.kwargs.get('User_ID'))
        if user_id_from_data:
            return user_id_from_data == request.user.id
        else:
            return True
