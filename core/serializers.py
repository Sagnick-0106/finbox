from rest_framework import serializers
from core.models import Stone, Activation
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class StoneSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Stone
        fields = "__all__"

    def get_status(self, obj):
        return "Active"


class ActivationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Activation
        fields = "__all__"


class ActivationListSerializer(ActivationSerializer):
    user_info = UserSerializer(source='User_ID', read_only=True)
    stone_info = StoneSerializer(source='Stone_ID', read_only=True)

    class Meta:
        model = Activation
        fields = ['Activation_ID', 'user_info', 'stone_info', 'Start_Time', 'End_Time']


class ActivationDataSerializer(serializers.Serializer):
    Stone_ID = serializers.IntegerField()
    User_ID = serializers.IntegerField()
    Power_Duration = serializers.IntegerField()
