# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-License-Identifier: MIT

"""Flask-Admin form utilities."""

from __future__ import absolute_import, print_function


class LazyChoices(object):
    """Lazy form choices."""

    def __init__(self, func):
        """Initialize lazy choices.

        :param func: Function returning an iterable of choices.
        """
        self._func = func

    def __iter__(self):
        """Iterate over lazy choices."""
        return iter(self._func())
