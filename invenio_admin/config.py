# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Configuration for Invenio-Admin."""

ADMIN_BASE_TEMPLATE = None
"""Admin panel base template.
By default (``None``) uses the Flask-Admin template."""

ADMIN_APPNAME = 'Invenio'
"""Name of the Flask-Admin app (also the page title of admin panel)."""

ADMIN_LOGIN_ENDPOINT = 'security.login'
"""Endpoint name of the login view. Anonymous users trying to access admin
panel will be redirected to this endpoint."""

ADMIN_LOGOUT_ENDPOINT = 'security.logout'
"""Endpoint name of logout view."""

ADMIN_TEMPLATE_MODE = 'bootstrap3'
"""Flask-Admin template mode. Either ``bootstrap2`` or ``bootstrap3``."""

ADMIN_PERMISSION_FACTORY = 'invenio_admin.permissions.admin_permission_factory'
"""Permission factory for the admin views."""
