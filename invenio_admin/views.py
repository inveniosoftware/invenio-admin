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

"""Admin view class factory for creating protected admin views on-the-fly."""

from __future__ import absolute_import, print_function

from flask import current_app, redirect, request, url_for
from flask_login import current_user
from werkzeug.local import LocalProxy

current_admin = LocalProxy(lambda: current_app.extensions['invenio-admin'])


def protected_adminview_factory(base_class):
    """Factory for creating protected admin view classes.

    The factory will create a new class using the provided class as base class
    and overwriting ``is_accessible()`` and ``inaccessible_callback()``
    methods.

    :param base_class: Class to use as base class.
    :returns: Admin view class which provides authentication and authorization.
    """
    class ProtectedAdminView(base_class):
        """Admin view class protected by authentication."""

        def is_accessible(self):
            """Require authentication and authorization."""
            return current_user.is_authenticated and \
                current_admin.permission_factory(self).can() and \
                super(ProtectedAdminView, self).is_accessible()

        def inaccessible_callback(self, name, **kwargs):
            """Redirect to login if user is not logged in."""
            if not current_user.is_authenticated:
                # Redirect to login page if user is not logged in.
                return redirect(url_for(
                    current_app.config['ADMIN_LOGIN_ENDPOINT'],
                    next=request.url))
            super(ProtectedAdminView, self).inaccessible_callback(
                name, **kwargs)

    return ProtectedAdminView
