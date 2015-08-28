# -*- coding: utf-8 -*-
"""
validate and serializer instance actions
"""
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from core import models
from service.action import get_action
from service.exceptions import ServiceException


class InstanceActionSerializer(serializers.ModelSerializer):
    action = PrimaryKeyRelatedField(
        queryset=models.InstanceAction.objects.all(),
        required=False, write_only=True)
    volume = PrimaryKeyRelatedField(queryset=models.Volume.active_volumes.all(),
                                    required=False, write_only=True)
    machine = PrimaryKeyRelatedField(
        queryset=models.ProviderMachine.objects.all(),
        required=False, write_only=True)
    size = PrimaryKeyRelatedField(queryset=models.Size.objects.all(),
                                  required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        self.provider = kwargs.pop("provider", None)
        super(InstanceActionSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        action = attrs.get("action")
        if not action.enabled_for_provider(self.provider):
            raise serializers.ValidationError(
                "The action `%s` is not enabled for the provider %s."
                % (action.name, instance.provider))
        return attrs

    class Meta:
        model = models.InstanceAction
        fields = (
            "id",
            "name",
            "description",
            "action",
            "volume",
            "machine",
            "size"
        )
