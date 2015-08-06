# -*- coding: utf-8 -*-
"""
Actions that can be performed by a provider
"""
import re

CLASS_NAME_REGEX = re.compile(
    '((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


class ActionManager(object):
    def __init__(self, actions):
        self.actions = {}
        for action_class in actions:
            assert issubclass(action_class, Action), (
                "Expected %s to be of type %s."
                % (action_class.__name__,
                   Action.__name__)
            )
            self.actions[action_class.identifier()] = action_class()

    def find(self, identifier):
        return self.actions.get(identifier)

    def get_catalog_info(self):
        catalog = []
        for action in self.actions.values():
            catalog.append(action.get_info())
        return catalog


class Action(object):
    name = None
    description = None

    @classmethod
    def identifier(cls):
        name = cls.__name__.rstrip("Action")
        return CLASS_NAME_REGEX.sub(r'-\1', name).lower()

    def validate(self, data=None):
        """
        Validates the action can be execute or fails
        """
        return False

    def execute(self, data=None):
        """
        Executes the action
        """

    def is_async(self):
        return False

    def get_info(self):
        return {"name": self.name, "description": self.description}
