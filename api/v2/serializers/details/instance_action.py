# -*- coding: utf-8 -*-
"""
validate and serializer instance actions
"""
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField


class InstanceActionSerializer(serializers.Serializer):
    action = serializers.SlugField(write_only=True)
    instance = PrimaryKeyRelatedField(queryset=Instance.objects.all(),
                                      write_only=True)
    data = serializers.DictField(child=serializers.CharField(),
                                 write_only=True)

    def __init__(self, *args, **kwargs):
        self.actions = kwargs.pop("actions")
        super(InstanceActionSerializer, self).__init__(*args, **kwargs)

    def validate_action(self, value):
        action = self.actions.get(value)
        if action is None:
            raise serializers.ValidationError(
                "The action `%s` does not exist." % value)
        return action

    class Meta:
        fields = ("action", "instance", "data")
