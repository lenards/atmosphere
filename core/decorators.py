# -*- coding: utf-8 -*-
"""
"""
from functools import wraps


def broken(message, logger):
    def broken_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except:
                logger.error(message)
                raise
        return wrapper
    return broken_decorator


def obsolete(message, logger):
    def obsolete_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            logger.warn(message)
            return fn(*args, **kwargs)
        return wrapper
    return obsolete_decorator
