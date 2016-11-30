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

"""Mocks of custom admin views for entrypoint testing."""

from flask_admin.base import BaseView, expose


class Four(BaseView):
    """AdminModelView of the ModelOne."""

    @expose('/')
    def index(self):
        """Index page."""
        return "Content of custom page Four"

four = dict(
    view_class=Four,
    kwargs=dict(
        category='Four',
        name='View number Four',
        endpoint='four',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-home')
    )
