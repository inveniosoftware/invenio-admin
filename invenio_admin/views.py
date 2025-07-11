# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2021 Northwestern University.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Admin view class factory for creating protected admin views on-the-fly."""

from __future__ import absolute_import, print_function

from flask import Blueprint, current_app, redirect, request, url_for
from flask_login import current_user

from .proxies import current_admin

blueprint = Blueprint(
    "invenio_admin",
    __name__,
)


def protected_adminview_factory(base_class):
    """Factory for creating protected admin view classes.

    The factory will ensure that the admin view will check if a user is
    authenticated and has the necessary permissions (as defined by the
    permission factory).
    The factory creates a new class using the provided class as base class
    and overwrites ``is_accessible()`` and ``inaccessible_callback()``
    methods. Super is called for both methods, so the base class can implement
    further restrictions if needed.

    :param base_class: Class to use as base class.
    :type base_class: :class:`flask_admin.base.BaseView`
    :returns: Admin view class which provides authentication and authorization.
    """

    class ProtectedAdminView(base_class):
        """Admin view class protected by authentication."""

        def _handle_view(self, name, **kwargs):
            """Override Talisman CSP header configuration for admin views.

            Flask-Admin extension is not CSP compliant (see:
            https://github.com/flask-admin/flask-admin/issues/1135).
            To avoid UI malfunctions, the CSP header (globally set on each
            request by Talisman extension) must be overridden and removed.
            Remove this code if and when Flask-Admin will be completely CSP
            compliant.
            """
            if invenio_app := current_app.extensions.get("invenio-app", None):
                # Because there seems to be back-and-forth on pinning and
                # unpinning dependencies, let's support both for now:
                if hasattr(invenio_app.talisman, "content_security_policy"):
                    invenio_app.talisman.content_security_policy = None
                else:
                    setattr(
                        invenio_app.talisman.local_options,
                        "content_security_policy",
                        None,
                    )
            return super(ProtectedAdminView, self)._handle_view(name, **kwargs)

        def is_accessible(self):
            """Require authentication and authorization."""
            return (
                current_user.is_authenticated
                and current_admin.permission_factory(self).can()
                and super(ProtectedAdminView, self).is_accessible()
            )

        def inaccessible_callback(self, name, **kwargs):
            """Redirect to login if user is not logged in.

            :param name: View function name.
            :param kwargs: Passed to the superclass' `inaccessible_callback`.
            """
            if not current_user.is_authenticated:
                # Redirect to login page if user is not logged in.
                return redirect(
                    url_for(
                        current_app.config["ADMIN_LOGIN_ENDPOINT"], next=request.url
                    )
                )
            super(ProtectedAdminView, self).inaccessible_callback(name, **kwargs)

    return ProtectedAdminView
