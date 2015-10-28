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
from flask_admin import Admin
from invenio_db import db

from . import config
from .views import ProtectedAdminIndexView, protected_adminview_factory


class InvenioAdmin(object):
    """Invenio-Admin extension.

    :param app: Flask application.
    :param entry_point_group: Name of entry point group to load views/models
        from.
    """

    def __init__(self, app=None, **kwargs):
        """Extension initialization."""
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group='invenio_admin.views',
                 **kwargs):
        """Flask application initialization."""
        self.init_config(app)

        # Create admin instance.
        self.admin = Admin(
            app,
            name=app.config['ADMIN_APPNAME'],
            template_mode=kwargs.get('template_mode', 'bootstrap3'),
            index_view=ProtectedAdminIndexView())

        # Load administration interfaces defined by entry points.
        if entry_point_group:
            for ep in pkg_resources.iter_entry_points(group=entry_point_group):
                modelview, model = ep.load()

                # Add default security to the model view
                protected_view = protected_adminview_factory(modelview)
                self.admin.add_view(protected_view(model, db.session))

        app.extensions['invenio-admin'] = self

    def init_config(self, app):
        """Initialize configuration."""
        # Set default configuration
        for k in dir(config):
            if k.startswith("ADMIN_"):
                app.config.setdefault(k, getattr(config, k))
