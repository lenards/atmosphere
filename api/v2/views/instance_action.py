from django.shortcuts import Http404

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from service.action import ActionManager


action_manager = ActionManager([])


class InstanceActionViewSet(viewsets.ViewSet):

    def list(self, request):
        """
        List of available actions to perform on an instance
        """
        return Response(data=action_manager.get_catalog_info())
