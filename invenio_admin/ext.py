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
from .views import ProtectedAdminIndexView, protected_adminview_factory


class InvenioAdmin(object):
    """Invenio-Admin extension.

    :param app: Flask application.
    :param entry_point_group: Name of entry point group to load views/models
        from.
    """

    def __init__(self, app=None, anonymous=False, **kwargs):
        """InvenioAdmin extension initialization.

        If `anonymous` is True, the admin views are accessible to anonymous
        users and all security checks are bypassed (use for testing only).
        """
        self.anonymous = anonymous
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group='invenio_admin.views',
                 **kwargs):
        """Flask application initialization."""
        self.init_config(app)

        # Create admin instance.
        index_view = AdminIndexView if self.anonymous \
            else ProtectedAdminIndexView
        self.admin = Admin(
            app,
            name=app.config['ADMIN_APPNAME'],
            template_mode=kwargs.get('template_mode', 'bootstrap3'),
            index_view=index_view())

        # Load administration interfaces defined by entry points.
        if entry_point_group:
            for ep in pkg_resources.iter_entry_points(group=entry_point_group):
                adminview_dict = dict(ep.load())
                assert 'model' in adminview_dict, \
                    "Admin's entrypoint dictionary must define the 'model'"
                assert 'modelview' in adminview_dict, \
                    "Admin's entrypoint dictionary must define the 'modelview'"
                model = adminview_dict.pop('model')
                modelview = adminview_dict.pop('modelview')

                # If not in anonymous access mode add model-based security
                if not self.anonymous:
                    modelview = protected_adminview_factory(modelview)
                self.admin.add_view(
                    modelview(model, db.session, **adminview_dict))
        app.extensions['invenio-admin'] = self

    def init_config(self, app):
        """Initialize configuration."""
        # Set default configuration
        for k in dir(config):
            if k.startswith("ADMIN_"):
                app.config.setdefault(k, getattr(config, k))
