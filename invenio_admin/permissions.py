# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2022 RERO.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Permissions for Invenio-Admin."""

import importlib_metadata
from flask_principal import ActionNeed

action_admin_access = ActionNeed("admin-access")
"""Define the action needed by the default permission factory."""


def admin_permission_factory(admin_view):
    """Default factory for creating a permission for an admin.

    It tries to load a :class:`invenio_access.permissions.Permission`
    instance if `invenio_access` is installed.
    Otherwise, it loads a :class:`flask_principal.Permission` instance.

    :param admin_view: Instance of administration view which is currently being
        protected.
    :returns: Permission instance.
    """
    try:
        importlib_metadata.version("invenio-access")
        from invenio_access import Permission
    except importlib_metadata.PackageNotFoundError:
        from flask_principal import Permission

    return Permission(action_admin_access)
