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


"""Module tests."""

from __future__ import absolute_import, print_function

import importlib

from flask import Flask
from flask_login import UserMixin, login_user
from mock import patch
from pkg_resources import EntryPoint

from invenio_admin import InvenioAdmin


def test_version():
    """Test version import."""
    from invenio_admin import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioAdmin(app)
    assert 'invenio-admin' in app.extensions

    app = Flask('testapp')
    ext = InvenioAdmin()
    assert 'invenio-admin' not in app.extensions
    ext.init_app(app)
    assert 'invenio-admin' in app.extensions


class TestUser(UserMixin):
    """Test user class."""

    def __init__(self, user_id):
        """Constructor of the user."""
        self.id = user_id

    @classmethod
    def get(cls, user_id):
        """Getter of the TestUser."""
        return cls(user_id)


def test_admin_view_authenticated(app):
    """Test the authentication for the admin."""
    login_manager = app.login_manager

    @login_manager.user_loader
    def load_user(user_id):
        return TestUser.get(user_id)

    @app.route('/login')
    def login():
        login_user(TestUser.get(1))
        return "Logged In"

    with app.test_client() as client:
        res = client.get("/admin", follow_redirects=True)
        assert res.status_code == 403
    with app.test_client() as client:
        res = client.get("/admin/testmodel", follow_redirects=True)
        assert res.status_code == 403

    with app.test_client() as client:
        res = client.get('/login', follow_redirects=True)
        res = client.get("/admin", follow_redirects=True)
        assert res.status_code == 200

    with app.test_client() as client:
        res = client.get('/login', follow_redirects=True)
        res = client.get("/admin/testmodel", follow_redirects=True)
        assert res.status_code == 200


class MockEntryPoint(EntryPoint):
    """Mock of EntryPoint."""

    def load(self):
        """Mock the load of entry point."""
        mod = importlib.import_module(self.module_name)
        obj = getattr(mod, self.name)
        return obj


def _mock_iter_entry_points(group=None):
    data = {
        'invenio_admin.views': [
            MockEntryPoint('one', 'demo.onetwo'),
            MockEntryPoint('two', 'demo.onetwo'),
            MockEntryPoint('three', 'demo.three'),
        ]
    }
    names = data.keys() if group is None else [group]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


@patch('pkg_resources.iter_entry_points', _mock_iter_entry_points)
def test_entry_points():
    """Test admin views discovery through entry points."""
    app = Flask('testapp')
    admin_app = InvenioAdmin(app)
    # Check if model views were added by checking the labels of menu items
    menu_items = [item.name for item in admin_app.admin.menu()]
    assert 'Model One' in menu_items
    assert 'Model Two' in menu_items
    assert 'Model Three' in menu_items
