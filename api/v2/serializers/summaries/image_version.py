from core.models import ApplicationVersion as ImageVersion
from rest_framework import serializers


class ImageVersionSummarySerializer(serializers.HyperlinkedModelSerializer):
    # Required when its a uuid -- otherwise LONGINT
    id = serializers.CharField(read_only=True)

    class Meta:
        model = ImageVersion
        view_name = 'api:v2:imageversion-detail'
        fields = ('id', 'url', 'name')
