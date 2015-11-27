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
"""Invenio-Admin is an administration interface for Invenio applications.

Invenio-Admin is an optional component of Invenio, responsible for registering
and customizing the administration panel for model views and user-defined
admin pages. The module uses standard Flask-Admin features and assumes very
little about other components installed within given Invenio instance.

Initialization
--------------
This section serves as an example on basic usage of the Invenio-Admin.
Create a basic Flask application (Flask-CLI is not needed for Flask 1.0 and up)

>>> from flask import Flask
>>> from flask_cli import FlaskCLI
>>> app = Flask('DinerApp')
>>> ext_cli = FlaskCLI(app)

InvenioDB is the only Invenio dependency which needs to be instantiated:

>>> from invenio_db import InvenioDB
>>> from invenio_admin import InvenioAdmin
>>> ext_db = InvenioDB(app)
>>> ext_admin = InvenioAdmin(app)

Let's now define a model and a model view ...

>>> from invenio_db import db
>>> from flask_admin.contrib.sqla import ModelView
>>> class Lunch(db.Model):
...     __tablename__ = 'diner_lunch'
...     id = db.Column(db.Integer, primary_key=True)
...     meal_name = db.Column(db.String(255), nullable=False)
...     is_vegetarian = db.Column(db.Boolean, default=False)
...
>>> class LunchModelView(ModelView):
...     can_create = True
...     can_edit = True
...

... and register them in the admin extension:

>>> ext_admin.register_view(LunchModelView, Lunch)

Finally, initialize the database and run the development server:

>>> from sqlalchemy_utils.functions import create_database
>>> app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
...     SECRET_KEY='SECRET')
...
>>> with app.app_context():
...     create_database(db.engine.url)
...     db.create_all()
>>> app.run() # doctest: +SKIP


You should now be able to access the admin panel `http://localhost:5000/admin
<http://localhost:5000/admin>`_.

Built-In security and authentication check
------------------------------------------
Although Invenio-Admin does not directly depend on Invenio-Access or
Invenio-Accounts module, it does protect the admin views with Flask-Login and
Flask-Principal features. In order to login to a Invenio-Admin panel the user
needs to be authenticated using Flask-Login and have a Flask-Principal
identity which provides the ``ActionNeed('admin-access')``.

AdminView discovery through setuptools' entry points
----------------------------------------------------
The default way of adding model views to admin panel in Invenio is though the
EntryPoint discovery. To do that, a newly created module has to register an
entry point under the group ``invenio_admin.views`` inside its ``setup.py``
as follows:

.. code-block:: Python

 # setup.py
 setup(
   entry_points={
       'invenio_admin.views': [
           'invenio_diner_snack = invenio_diner.admin.snack_adminview',
           'invenio_diner_breakfast = invenio_diner.admin.breakfast_adminview',
       ]
   },
 )

The example above will add two model views to Invenio-Admin instance, namely
the description of ``Snack`` and ``Breakfast`` models.
Definitions of model views are usually defined inside a file
``invenio-diner/invenio_diner/admin.py``:

A typical example of the admin view definition is as follows:

.. code-block:: Python

 # admin.py
 from flask_admin.contrib.sqla import ModelView
 from flask_babelex import gettext as _
 from .models import Snack, Breakfast

 class SnackModelView(ModelView):
     can_create = True
     can_edit = True
     can_view_details = True
     column_list = ('name', 'price', )

 class BreakfastModelView(ModelView):
     can_create = False
     can_edit = False
     can_view_details = True
     column_searchable_list = ('toast', 'eggs', 'bacon' )

 snack_adminview = {'model':Snack,
                    'modelview': SnackModelView,
                    'category': 'Diner'}
 breakfast_adminview = {'model':Breakfast,
                        'modelview': BreakfastModelView,
                        'category': 'Diner'}
 __all__ = (
     'snack_adminview',
     'breakfast_adminview',
 )

The dictionary specifying given admin view is required to contain keys
``model`` and ``modelview``, which should point to class definitions of
database Model and admin ModelView. The remaining keys are passed as keyword
arguments to the constructor of flask_admin.contrib.sqla.ModelView.

"""

from __future__ import absolute_import, print_function

from .ext import InvenioAdmin
from .version import __version__

__all__ = ('__version__', 'InvenioAdmin')
