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

"""Invenio-Admin is an administration interface for Invenio applications.

Invenio-Admin is an optional component of Invenio, responsible for registering
and customizing the administration panel for model views and user-defined
admin pages. The module uses standard Flask-Admin features and assumes very
little about other components installed within a given Invenio instance.

Quick start
-----------
This section presents a minimal working example of the Invenio-Admin usage.

First, let us create a new Flask application:

>>> from flask import Flask
>>> app = Flask('DinerApp')

and load the Invenio-DB (required for model views)
and Invenio-Admin extensions:

>>> from invenio_db import InvenioDB
>>> from invenio_admin import InvenioAdmin
>>> ext_db = InvenioDB(app)
>>> ext_admin = InvenioAdmin(app)

Let's now define a simple model with a model view, as well as simple base view:

>>> from invenio_db import db
>>> from flask_admin.contrib.sqla import ModelView
>>> from flask_admin.base import BaseView, expose
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
>>> class MyBaseView(BaseView):
...     @expose('/')
...     def index(self):
...         return "HelloWorld!"

and register them in the admin extension:

>>> ext_admin.register_view(LunchModelView, Lunch)
>>> ext_admin.register_view(MyBaseView)

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

Adding admin views from Invenio module
--------------------------------------
In real-world scenarios you will most likley want to add an admin view for
your custom models from within the Invenio module or an Invenio overlay
application. Instead of registering it directly on the application as in the
example above, you can use entry points to register those automatically.

Defining admin views
~~~~~~~~~~~~~~~~~~~~
Let us start with defining the ``admin.py`` file inside your module or overlay,
which will contain all admin-related classes and functions.
For example, assuming a ``Invenio-Diner`` module, the file could reside in:

``invenio-diner/invenio_diner/admin.py``.

In this example we will define two ModelViews for two ORM models and one
separate BaseView for statistics. The content of the file is as follows:

.. code-block:: python

    # invenio-diner/invenio_diner/admin.py
    from flask_admin.contrib.sqla import ModelView
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

    class DinerStats(BaseView):
        @expose('/')
        def index(self):
            return "Welcome to the Invenio Diner Statistics page!"

        @expose('/sales/')
        def sales(self):
            return "You have served 0 dinners!"

    snack_adminview = {
        'model': Snack,
        'modelview': SnackModelView,
        'category': 'Diner',
    }

    breakfast_adminview = {
        'model': Breakfast,
        'modelview': BreakfastModelView,
        'category': 'Diner',
    }

    stats_adminview = {
        'view': DinerStats,
        'name': 'Invenio Diner Stats',
    }

    __all__ = (
        'snack_adminview',
        'breakfast_adminview',
        'stats_adminview',
    )

.. note::

    You have to define a dictionary for each BaseView and Model-ModelView pairs
    (see ``stats_adminview``, ``snack_adminview`` and ``breakfast_adminview``
    above).

    For ModelViews, the dictionary has to contain the keys ``model`` and
    ``modelview``, which should point to class definitions of database model
    and admin ModelView class.

    For BaseViews the dictionary should specify a ``view`` key, which should
    point to a custom BaseView class.

    All keys other than ``view``, ``model`` and ``modelview`` are passed as
    keyword arguments to the constructors of
    :class:`flask_admin.contrib.sqla.ModelView` and
    :class:`flask_admin.base.BaseView`.

Registering the entry point
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The default way of adding admin views to the admin panel is though the
setuptools entry point discovery. To do that, a newly created module has to
register an entry point under the group ``invenio_admin.views`` inside its
``setup.py`` as follows:

.. code-block:: python

    # invenio-diner/setup.py
    setup(
      entry_points={
        'invenio_admin.views': [
          'invenio_diner_snack = invenio_diner.admin.snack_adminview',
          'invenio_diner_breakfast = invenio_diner.admin.breakfast_adminview',
          'invenio_diner_stats = invenio_diner.admin.stats_adminview',
        ],
      },
    )


Security and authentication check
---------------------------------
By default Invenio-Admin protects the admin views from un-authenticated users
with Flask-Login and restricts the access on a per-permission basis using
Flask-Security. In order to login to a Invenio-Admin panel the user
needs to be authenticated using Flask-Login and have a Flask-Security
identity which provides the ``ActionNeed('admin-access')``.

.. note::

    If you want to use a custom permission rule, you can easily set
    provide your own permission factory in the configuration variable
    :data:`invenio_admin.config.ADMIN_PERMISSION_FACTORY`.

    For more information see the factory:
    :func:`invenio_admin.permissions.admin_permission_factory`
    and the view using it:
    :func:`invenio_admin.views.protected_adminview_factory`


Styling
-------
Base template
~~~~~~~~~~~~~
Styling of the administration interface can be changed via the configuration
variable ``ADMIN_BASE_TEMPLATE``.

If Invenio-Theme is installed,
``ADMIN_BASE_TEMPLATE`` is automatically set to use the
`AdminLTE <https://almsaeedstudio.com/themes/AdminLTE/index2.html>`_ theme
which provides an extra configuration variable ``ADMIN_UI_SKIN`` which controls
the AdminLTE skin (e.g. ``skin-blue`` or ``skin-black``). See AdminLTE
documentation for details on supported skins.

If Invenio-Theme is not installed the default Flask-Admin templates will be
used (based on Bootstrap).

View template mode
~~~~~~~~~~~~~~~~~~
Flask-Admin view templates (forms etc.) can either use Bootstap 2 or 3. By
default the template mode is set to Bootstrap 3 but can be controlled through
``ADMIN_TEMPLATE_MODE`` configuration variable.
"""

from __future__ import absolute_import, print_function

from .ext import InvenioAdmin
from .proxies import current_admin
from .version import __version__

__all__ = ('__version__', 'InvenioAdmin')
