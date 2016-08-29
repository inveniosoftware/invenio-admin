# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Permissions for Invenio-Admin."""

import pkg_resources
from flask_principal import ActionNeed

action_admin_access = ActionNeed('admin-access')
"""Define the action needed by the default permission factory."""


def admin_permission_factory(admin_view):
    """Default factory for creating a permission for an admin.

    It tries to load a :class:`invenio_access.permissions.DynamicPermission`
    instance if `invenio_access` is installed.
    Otherwise, it loads a :class:`flask_principal.Permission` instance.

    :param admin_view: Instance of administration view which is currently being
        protected.
    :returns: Permission instance.
    """
    try:
        pkg_resources.get_distribution('invenio-access')
        from invenio_access.permissions import DynamicPermission as Permission
    except pkg_resources.DistributionNotFound:
        from flask_principal import Permission

    return Permission(action_admin_access)
