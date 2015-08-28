# -*- coding: utf-8 -*-
"""
Actions that can be performed by a provider
"""
from core import models
from service.driver import create_driver
from service.exceptions import ServiceException
from service import instance, volume


actions = {
#    "attach_volume": {
#        "name": "Attach Volume",
#        "description": "Attach the volume to the instance.",
#        "action": instance.attach_volume
#    },
#    "confirm_resize": {
#        "name": "Confirm Resize",
#        "description": "Confirm the instance works after a resize.",
#        "action": instance.confirm_resize
#    },
    "console": {
        "name": "Console",
        "description": "Get the console for an instance.",
        "action": instance.get_console
    }
#    "deploy": {
#        "name": "Deploy instance",
#        "description": "Run deployment scripts for the instance.",
#        "action": instance.deploy
#    },
#    "detach_volume": {
#        "name": "Deattach volume",
#        "description": "Detach the volume from the instance.",
#        "action": instance.detach_volume
#    },
#    "mount_volume": {
#        "name": "Mount Volume",
#        "description": "Mount the volume to the instance."
#        "action": instance.mount_volume
#    },
#    "rebuild": {
#        "name": "Rebuild Instance",
#        "description": "Rebuild the given instance.",
#        "action": instance.rebuild_instance
#    },
#    "reset_network": {
#        "name": "Reset Networking",
#        "description": "Reset the networking on an instance.",
#        "action": instance.reset_networking
#    },
#    "resize": {
#        "name": "Resize Instance",
#        "description": "Resize the instance to the given size.",
#        "action": instance.resize
#    },
#    "resume": {
#        "name": "Resume Instance",
#        "description": "Resume the instance if suspended."
#        "action": instance.resume
#    },
#    "revert_size": {
#        "name": "Revert Size",
#        "description": "Revert the instance if resizing fails.",
#        "action": instance.revert_size
#    },
#    "shelve_offload": {
#        "name": "Shelve Off Load",
#        "description": "Offload the shelved instance"
#        "action": instance.shelve_offload
#    },
#    "start": {
#        "name": "Start Instance",
#        "description": "Start a stopped instance"
#        "action": instance.start
#    },
#    "shelve": {
#        "name":  "Shelve instance",
#        "description": "Shelves aninstance for an extended period",
#        "action": instance.shelve
#    },
#    "stop": {
#        "name": "Stop Instance",
#        "description": "Stop a running instance",
#        "action": instance.stop
#    },
#    "suspend": {
#        "name": "Suspend Instance",
#        "description": "Suspend the instance if running.",
#        "action": instance.suspend
#    },
#    "unmount_volume": {
#        "name": "Unmount Volume",
#        "description": "Unmount the volume from the instance."
#        "action": instance.unmount_volume
#    },
#    "unshelve": {
#        "name": "Unshelve Instance",
#        "description": "Unshelve a instance previously shelved.",
#        "action": instance.unshelve
#    }
}


def get_action(instance_action):
    try:
        return actions[instance_action.identifier]
    except:
        raise ServiceException("Action %s could not be found." % action_name)
