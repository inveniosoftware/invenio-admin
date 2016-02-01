# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

"""Invenio-Admin Flask extension."""

from __future__ import absolute_import, print_function

import pkg_resources
from flask_admin import Admin, AdminIndexView
from invenio_db import db

from . import config
from .permissions import admin_permission_factory
from .views import protected_adminview_factory


class _AdminState(object):
    """State for Invenio-Admin."""

    def __init__(self, app, admin, permission_factory, view_class_factory):
        """Initialize state."""
        # Create admin instance.
        self.app = app
        self.admin = admin
        self.permission_factory = permission_factory
        self.view_class_factory = view_class_factory

    def register_view(self, view_class, model_class, session=None, **kwargs):
        """Register an admin view on this admin instance."""
        view_class = self.view_class_factory(view_class)
        self.admin.add_view(
            view_class(model_class, session or db.session, **kwargs))

    def load_entry_point_group(self, entry_point_group):
        """Load administration interface from entry point group."""
        for ep in pkg_resources.iter_entry_points(group=entry_point_group):
            admin_ep = dict(ep.load())
            assert 'model' in admin_ep, \
                "Admin's entrypoint dictionary must define the 'model'"
            assert 'modelview' in admin_ep, \
                "Admin's entrypoint dictionary must define the 'modelview'"

            self.register_view(
                admin_ep.pop('modelview'),
                admin_ep.pop('model'),
                **admin_ep)


class InvenioAdmin(object):
    """Invenio-Admin extension.

    :param app: Flask application.
    :param entry_point_group: Name of entry point group to load views/models
        from.
    :param permission_factory: Default permission factory to use when
        protecting admin view.
    :param viewcls_factory: Factory for creating admin view classes on the
        fly. Used to protect admin views with authentication and authorization.
    :param indeview_cls: Admin index view class.
    """

    def __init__(self, app=None, **kwargs):
        """Invenio-Admin extension initialization."""
        if app:
            self._state = self.init_app(app, **kwargs)

    def init_app(self,
                 app,
                 entry_point_group='invenio_admin.views',
                 permission_factory=admin_permission_factory,
                 view_class_factory=protected_adminview_factory,
                 index_view_class=AdminIndexView,
                 **kwargs):
        """Flask application initialization."""
        self.init_config(app)

        # Create administration app.
        admin = Admin(
            app,
            name=app.config['ADMIN_APPNAME'],
            template_mode=kwargs.get('template_mode', 'bootstrap3'),
            index_view=view_class_factory(index_view_class)())

        # Create admin state
        state = _AdminState(app, admin, permission_factory, view_class_factory)
        if entry_point_group:
            state.load_entry_point_group(entry_point_group)

        app.extensions['invenio-admin'] = state
        return state

    def init_config(self, app):
        """Initialize configuration."""
        # Set default configuration
        for k in dir(config):
            if k.startswith("ADMIN_"):
                app.config.setdefault(k, getattr(config, k))

    def __getattr__(self, name):
        """Proxy to state object."""
        return getattr(self._state, name, None)
