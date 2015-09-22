from core.models import Identity, Group, IdentityMembership
from core.models.group import IdentityMembershipHistory
from core.query import only_current_provider

from api.v2.serializers.details import IdentitySerializer
from api.v2.views.base import AuthViewSet

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import detail_route


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityMembershipHistory
        fields = (
            'field_name',
            'operation',
            'current_value',
            'previous_value',
            'timestamp'
        )


class IdentityViewSet(AuthViewSet):

    """
    API endpoint that allows providers to be viewed or edited.
    """
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    http_method_names = ['get', 'head', 'options', 'trace']

    def get_queryset(self):
        """
        Filter identities by current user
        """
        user = self.request.user
        group = Group.objects.get(name=user.username)
        identities = group.identities.filter(
            only_current_provider(), provider__active=True)
        return identities

    @detail_route(methods=['get'])
    def changes(self, request, pk=None):
        identity = self.get_object()
        membership = IdentityMembership.objects.get(identity=identity)
        changes = IdentityMembershipHistory.objects.filter(membership=membership)
        serializer = HistorySerializer(changes, many=True)
        return Response(serializer.data)
