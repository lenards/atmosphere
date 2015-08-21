# -*- coding: utf-8 -*-
"""
"""
from functools import wraps


def broken(message):
    def broken_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            logger.error(message)
            return fn(*args, **kwargs)
        return wrapper
    return broken_decorator


def obsolete(message):
    def obsolete_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            logger.warn(message)
            return fn(*args, **kwargs)
        return wrapper
    return obsolete_decorator
