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

"""Mocks of DB Models and Admin's ModelViews for entrypoint testing."""

from flask_admin.contrib.sqla import ModelView
from invenio_db import db


class ModelOne(db.Model):
    """Test model with just one column."""

    id = db.Column(db.Integer, primary_key=True)
    """Id of the model."""


class ModelTwo(db.Model):
    """Test model with just one column."""

    id = db.Column(db.Integer, primary_key=True)
    """Id of the model."""


class ModelOneModelView(ModelView):
    """AdminModelView of the ModelOne."""

    pass


class ModelTwoModelView(ModelView):
    """AdminModelView of the ModelTwo."""

    pass

# Invalid admin entry point:
zero = {}

# Old deprecated way of specifying admin entry points:
one = dict(
    modelview=ModelOneModelView,
    model=ModelOne,
    category='OneAndTwo'
)
# New way of specifying admin entry points:
two = dict(
    view_class=ModelTwoModelView,
    args=[ModelTwo, db.session],
    kwargs=dict(category='OneAndTwo')
 )
