# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-License-Identifier: MIT

"""Mocks of DB Models and Admin's ModelViews for entrypoint testing."""

from flask_admin.contrib.sqla import ModelView
from invenio_db import db


class ModelThree(db.Model):
    """Test model with just one column."""

    id = db.Column(db.Integer, primary_key=True)
    """Id of the model."""


class ModelThreeModelView(ModelView):
    """AdminModelView of the ModelOne."""

    pass


three = dict(modelview=ModelThreeModelView, model=ModelThree)
