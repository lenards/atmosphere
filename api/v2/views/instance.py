from rest_framework.response import Response
from rest_framework.decorators import detail_route

from core.models import Instance
from core.models.provider import ProviderInstanceAction
from api.v2.serializers.details import InstanceSerializer,\
    InstanceActionSerializer
from core.query import only_current

from api.v1.views.instance import Instance as V1Instance

from api.v2.views.base import AuthViewSet
from service.action import get_action


class InstanceViewSet(AuthViewSet):

    """
    API endpoint that allows providers to be viewed or edited.
    """

    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    filter_fields = ('created_by__id', 'projects')
    http_method_names = ['get', 'put', 'patch', 'head', 'options', 'trace']

    def get_queryset(self):
        """
        Filter projects by current user.
        """
        user = self.request.user
        if 'archived' in self.request.QUERY_PARAMS:
            return Instance.objects.filter(created_by=user)
        return Instance.objects.filter(only_current(), created_by=user)

    def perform_destroy(self, instance):
        return V1Instance().delete(self.request,
                                   instance.provider_alias,
                                   instance.created_by_identity.uuid,
                                   instance.id)

    @detail_route(methods=['get'], url_path="action")
    def show_actions(self, request, pk=None):
        instance = self.get_object()
        provider_actions = ProviderInstanceAction.objects.filter(
                provider=instance.provider, enabled=True)
        actions = (pa.instance_action for pa in provider_actions)
        serializer = InstanceActionSerializer(actions, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'], url_path="action")
    def submit_action(self, request, pk=None):
        instance = self.get_object()
        serializer = InstanceActionSerializer(data=self.request.data,
                                              provider=instance.provider)
        serializer.is_valid(raise_exception=True)
        try:
            action = get_action(serializer.validated_data.pop("action"))
            driver = create_driver(instance.created_by_identity)
            return Response(data=action(driver=driver, instance=instance,
                                        **data))
        except Exception as e:
            raise exceptions.ParseError(detail=e.message)
