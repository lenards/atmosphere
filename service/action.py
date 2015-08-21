# -*- coding: utf-8 -*-
"""
Actions that can be performed by a provider
"""
import re

CLASS_NAME_REGEX = re.compile(
    '((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

def create_action_manager():
    catalog = (
        #actions.AttachVolumeAction,
        #actions.MountVolumeAction,
        #actions.UnmountVolumeAction,
        #actions.DetachAction,
        #actions.ResizeAction,
        #actions.ConfirmResizeAction,
        #actions.RevertSizeAction,
        #actions.SuspendAction,
        #actions.DeployAction,
        #actions.ResumeAction,
        #actions.StartAction,
        #actions.StopAction,
        #actions.ShelveAction,
        #actions.UnshelveAction,
        #actions.ShelveOffLoadAction,
        #actions.RebootAction,
        #actions.ConsoleAction,
        #actions.ResetNetworkAction,
        #actions.RebuildAction,
    )
    return ActionManager(actions=catalog)


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


class ValidatorMixin(object):
    def validate_instance(self, instance):
        if not isinstance(instance, models.Instance):
            raise ServiceException("Invalid instance")

    def validate_volume(self, volume):
        if not isinstance(volume, models.Volume):
            raise ServiceException("Invalid volume")

    def validate_machine(self, machine):
        if not isinstance(machine, models.ProviderMachine):
            raise ServiceException("Invalid machine")

    def validate_size(self, size):
        if not isinstance(size, models.Size):
            raise ServiceException("Invalid size")


class Action(ValidatorMixin):
    name = None
    description = None

    @classmethod
    def identifier(cls):
        name = cls.__name__.rstrip("Action")
        return CLASS_NAME_REGEX.sub(r'-\1', name).lower()

    def execute(self, data=None):
        """
        Executes the action
        """
        assert hasattr(self, "validate_data"), (
            "%s should have attribute `validate_data`."
            % self.__class__.__name__
        )
        assert hasattr(self, "perform_action"), (
            "%s should have attribute `perform_action`."
            % self.__class__.__name__
        )
        driver = create_driver(identity)
        validated_data = self.validate_data(data)
        return self.perform_action(driver, validated_data)

    def get_info(self):
        return {"action": self.identifier(),
                "name": self.name,
                "description": self.description}
