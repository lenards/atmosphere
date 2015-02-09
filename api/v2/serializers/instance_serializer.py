from core.models import Instance
from rest_framework import serializers
from .identity_summary_serializer import IdentitySummarySerializer
from .user_serializer import UserSerializer
from .provider_summary_serializer import ProviderSummarySerializer


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    identity = IdentitySummarySerializer(source='created_by_identity')
    user = UserSerializer(source='created_by')
    provider = ProviderSummarySerializer(source='created_by_identity.provider')

    class Meta:
        model = Instance
        view_name = 'api_v2:instance-detail'
        fields = ('id', 'url', 'name', 'ip_address', 'shell', 'vnc', 'start_date', 'end_date', 'identity', 'user', 'provider')
