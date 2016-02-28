# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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

"""Filters module tests."""

from __future__ import absolute_import, print_function

import uuid

from invenio_admin.filters import FilterConverter, UUIDEqualFilter


def test_uuid_filter(app, testmodelcls):
    """Test UUID."""
    with app.app_context():
        f = UUIDEqualFilter(testmodelcls.uuidcol, 'uuidcol')
        q = testmodelcls.query
        assert q.whereclause is None

        q_applied = f.apply(testmodelcls.query, str(uuid.uuid4()), None)
        assert q_applied.whereclause is not None

        q_applied = f.apply(testmodelcls.query, "", None)
        assert q_applied.whereclause is None

        q_applied = f.apply(testmodelcls.query, "test", None)
        assert q_applied.whereclause is None


def test_filter_converter_uuid(testmodelcls):
    """Test filter converter."""
    c = FilterConverter()
    f = c.convert('uuidtype', testmodelcls.uuidcol, 'uuidcol')
    assert len(f) == 1
    assert isinstance(f[0], UUIDEqualFilter)


def test_filter_converter_variant(testmodelcls):
    """Test filter converter."""
    c = FilterConverter()
    f = c.convert('variant', testmodelcls.dt, 'dt')
    assert len(f) == 7
