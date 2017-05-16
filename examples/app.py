# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2017 CERN.
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

"""Minimal Flask application example for development.

SPHINX-START

First, install Invenio-Admin, setup the application and load fixture data by
running:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

Next, start the development server:

.. code-block:: console

   $ export FLASK_APP=app.py FLASK_DEBUG=1
   $ flask run

and open the example application in your browser:

.. code-block:: console

    $ open http://127.0.0.1:5000/

To reset the example application run:

.. code-block:: console

    $ ./app-teardown.sh

SPHINX-END
"""

from __future__ import absolute_import, print_function

from flask import Flask, Markup, flash, redirect
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_mail import Mail
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint as accounts_blueprint
from invenio_assets import InvenioAssets
from invenio_db import InvenioDB, db
from invenio_i18n import InvenioI18N
from invenio_theme import InvenioTheme

from invenio_admin import InvenioAdmin
from invenio_admin.views import blueprint as admin_blueprint
from invenio_admin.views import protected_adminview_factory

# Create Flask application
app = Flask(__name__)
app.config.update(
    ACCOUNTS_USE_CELERY=False,
    CELERY_ALWAYS_EAGER=True,
    CELERY_CACHE_BACKEND='memory',
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_RESULT_BACKEND='cache',
    MAIL_SUPPRESS_SEND=True,
    SECRET_KEY='CHANGE_ME',
    SECURITY_PASSWORD_SALT='CHANGE_ME_ALSO',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    WTF_CSRF_ENABLED=False,
)

Babel(app)
Mail(app)
InvenioDB(app)
InvenioAccounts(app)
InvenioAccess(app)
InvenioAssets(app)
InvenioI18N(app)
InvenioTheme(app)
admin_app = InvenioAdmin(app)
app.register_blueprint(accounts_blueprint)
app.register_blueprint(admin_blueprint)


@app.route('/')
def index():
    """Basic test view."""
    flash(Markup(
        'Login with username <strong>info@inveniosoftware.org</strong> '
        'and password <strong>123456</strong>.'
    ))
    return redirect('/admin/')


class TestModel(db.Model):
    """Simple model with just one column."""

    id = db.Column(db.Integer, primary_key=True)
    """Id of the model."""


class TestModelView(ModelView):
    """ModelView of the TestModel."""


protected_view = protected_adminview_factory(TestModelView)
admin_app.admin.add_view(protected_view(TestModel, db.session))
