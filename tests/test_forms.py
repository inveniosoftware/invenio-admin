# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-License-Identifier: MIT

"""Form module tests."""

from __future__ import absolute_import, print_function

from invenio_admin.forms import LazyChoices


def test_lazy_choices():
    """Test lazy choices."""
    called = dict(val=False)

    def _choices():
        called["val"] = True
        return [1, 2]

    choices = LazyChoices(_choices)
    assert not called["val"]
    assert list(choices) == [1, 2]
    assert called["val"]
