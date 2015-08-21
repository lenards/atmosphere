from django.shortcuts import Http404

from rest_framework import viewsets
from rest_framework import status
from rest_framework import exceptions
from rest_framework.response import Response

from api.permissions import CanEditOrReadOnly
from api.v2.serializers.details import InstanceActionSerializer
from core.models import Instance
from service.action import create_action_manager

action_manager = create_action_manager()


class InstanceActionViewSet(viewsets.ViewSet):
    def check_permission(self, request, obj):
        permission = CanEditOrReadOnly()
        if not permission.has_object_permission(request, self, obj):
            raise exceptions.PermissionDenied()

    def create(self, request):
        """
        Runs an instance action
        """
        serializer = InstanceActionSerializer(data=self.request.data,
                                              actions=action_manager.actions)
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data.get("instance")
        self.check_permission(request, instance)
        response = self.perform_create(serializer)
        return Response(data=response)

    def list(self, request):
        """
        List of available actions to perform on an instance
        """
        return Response(data=action_manager.get_catalog_info())

    def perform_create(self, serializer):
        """
        Executes the instance action
        """
        try:
            action = serializer.validated_data.get("action")
            identity = serializer.validated_data.pop("identity")
            data = serializer.validated_data.get("data", {})
            return action.execute(identity, data=data)
        except Exception as e:
            raise exceptions.ParseError(detail=e.message)
