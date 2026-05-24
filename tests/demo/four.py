# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-License-Identifier: MIT

"""Mocks of custom admin views for entrypoint testing."""

from flask_admin.base import BaseView, expose


class Four(BaseView):
    """AdminModelView of the ModelOne."""

    @expose("/")
    def index(self):
        """Index page."""
        return "Content of custom page Four"


four = dict(
    view_class=Four,
    kwargs=dict(
        category="Four",
        name="View number Four",
        endpoint="four",
        menu_icon_type="glyph",
        menu_icon_value="glyphicon-home",
    ),
)
