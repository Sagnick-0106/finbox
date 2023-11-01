from datetime import timedelta

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from core.serializers import ActivationListSerializer, ActivationDataSerializer
from core.tasks import asynchronous_task, activate_stone
from core.models import Activation, Stone
from core.permissions import MatchUserIdPermission


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, MatchUserIdPermission])
class DefaultViewSet(viewsets.ModelViewSet):
    queryset = Activation.objects.all()

    def home(self, request):
        return Response({"message": "Server is up and running."})

    def submit_task(self, request):
        result = asynchronous_task.delay(2, 3)

        # Respond immediately to the client
        response_data = {
            'task_id': result.id,
            'message': 'Task is being processed asynchronously.',
        }
        return JsonResponse(response_data)

    def user_status(self, request, *args, **kwargs):
        user_id = self.kwargs.get('User_ID')
        # Get the current time
        current_time = timezone.now()
        active_stone = self.queryset.filter(User_ID=user_id, End_Time__gt=current_time)
        user_info = get_user_model().objects.get(id=user_id)
        if active_stone:
            serializer = ActivationListSerializer(active_stone, many=True)
            return Response(serializer.data)

        response_data = {
            "message": f"Sorry {user_info.username}, no stones are in your control as of now."
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    def activate(self, request, *args, **kwargs):
        serializer = ActivationDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stone_id = request.data.get('Stone_ID')
        user_id = request.data.get('User_ID')
        user_info = get_user_model().objects.get(id=user_id)
        stone_info = Stone.objects.get(Stone_ID=stone_id)
        current_time = timezone.now()
        # Check if This stone is active
        activated = self.queryset.filter(Stone_ID=stone_id, End_Time__gt=current_time)
        if activated:
            if activated[0].User_ID_id == user_id:
                response_data = {
                    "message":
                        f"{user_info.username}!! You are the lord of {stone_info.Stone_Name} now."
                }
            else:
                response_data = {
                    "message":
                        f"{user_info.username}!! You can not activate {stone_info.Stone_Name}, as it is already active."
                }
            return JsonResponse(response_data)
        # Check if user has activated any other stone
        self_activated = self.queryset.filter(User_ID=user_id, End_Time__gt=current_time)
        if self_activated:
            response_data = {
                "message":
                    f"{user_info.username}!! You already activated {self_activated[0].Stone_ID.Stone_Name}, as a result"
                    f" you can not activate {stone_info.Stone_Name}."
            }
            return JsonResponse(response_data)

        duration = request.data.get('Power_Duration')
        data = {
            "Stone_ID": stone_id,
            "User_ID": user_id,
            "Start_Time": timezone.now(),
            "End_Time": timezone.now() + timedelta(seconds=duration)
        }

        activate_stone.delay(data, stone_id, user_info.username)

        response_data = {
            "message": f"{user_info.username}!! You are about to activate {stone_info.Stone_Name}."
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
