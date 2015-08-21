# -*- coding: utf-8 -*-
"""
validate and serializer instance actions
"""
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from core import models

class InstanceActionSerializer(serializers.Serializer):
    action = serializers.SlugField(write_only=True)
    instance = PrimaryKeyRelatedField(queryset=models.Instance.objects.all(),
                                      write_only=True)
    volume = PrimaryKeyRelatedField(queryset=models.Volume.objects.all(),
                                    required=False, write_only=True)
    machine = PrimaryKeyRelatedField(
        queryset=models.ProviderMachine.objects.all(),
        required=False, write_only=True)
    size = PrimaryKeyRelatedField(queryset=models.Size.objects.all(),
                                  required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        self.actions = kwargs.pop("actions")
        super(InstanceActionSerializer, self).__init__(*args, **kwargs)

    def validate_action(self, value):
        action = self.actions.get(value)
        if action is None:
            raise serializers.ValidationError(
                "The action `%s` does not exist." % value)
        return action

    def validate(self, values):
        action = values.pop("action")
        attrs = {"action": action}
        try:
            attrs["data"] = action.validate_data(values)
        except ServiceException as e:
            raise serializers.ValidationError(e.message)
        return attrs

    class Meta:
        fields = ("action", "instance")
