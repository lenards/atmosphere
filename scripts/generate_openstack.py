#!/usr/bin/env python

from atmosphere.settings import secrets
from service.accounts.openstack import AccountDriver
from core.models import AtmosphereUser as User
from keystoneclient.exceptions import NotFound
import django
django.setup()


def main():
    """
    Generate openstack users then add them to the DB
    """
    driver = AccountDriver(secrets.OPENSTACK_ARGS)
    # Build the admin driver for openstack first.
    driver.create_identity(
        secrets.OPENSTACK_ADMIN_KEY,
        secrets.OPENSTACK_ADMIN_SECRET,
        secrets.OPENSTACK_ADMIN_TENANT,
        True)
    success = 1
    # Add the others
    # 'sgregory', 'jmatt', 'edwins', 'cjlarose','mlent']
    core_services = ['atmo_test']
    for username in core_services:
        try:
            password = driver.hashpass(username)
            user = driver.get_user(username)
            if not user:
                user = driver.create_user(username, usergroup=True)
                print 'New OStack User - %s Pass - %s' % (user.name, password)
            else:
                print 'Found OStack User - %s Pass - %s' % (user.name, password)
            # ASSERT: User exists on openstack, create an identity for them.
            ident = driver.create_identity(
                user.name,
                password,
                project_name=username)
            success += 1
            print 'New OStack Identity - %s:%s' % (ident.id, ident)
        except Exception as e:
            print "Problem adding username: %s" % username
            print e
            raise

    print "Total users created:%s/%s" % (success, len(core_services))

if __name__ == "__main__":
    main()
