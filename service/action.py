# -*- coding: utf-8 -*-
"""
Actions that can be performed by a provider
"""
from core import models
from service.driver import create_driver
from service.exceptions import ServiceException
from service import instance, volume


actions = {
    "console": {
        "name": "Console",
        "description": "Get the console for an instance.",
        "action": instance.get_console
    },
    "reset_network": {
        "name": "Reset Networking",
        "description": "Reset the networking on an instance.",
        "action": instance.reset_networking
    },
    "rebuild": {
        "name": "Rebuild Instance",
        "description": "Rebuild the given instance.",
        "action": instance.rebuild_instance
    }
}


def get_action(action_name):
    try:
        return actions[action_name]
    except:
        raise ServiceException("Action %s could not be found." % action_name)

    "attach_volume": {
        "name": "Attach volume",
        "description": "Attach a given volume to an instance",
        "action": attach_volume
    }
