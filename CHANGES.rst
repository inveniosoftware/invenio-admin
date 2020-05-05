..
    This file is part of Invenio.
    Copyright (C) 2015-2018 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 1.1.3 (released 2020-05-05)

- Minimum version of Invenio-Accounts bumped to v1.1.4 due WTForms moving the
  email validation to an optional dependency.
- Minimum version of Flask-Admin bumped to v1.5.6 due to a fixed SQLAlchemy
  1.3.6 compatibility issue
- Maximum version of Invenio-Access set to 1.4.0 due to circular dependency.
- Minimum version of Flask bumped to 1.0.4 and from six to 1.12.0 due to
  dependency management missmatches.
- Maximum version of Flask-Login set to 0.5.0 due to dependency management
  missmatches.

Version 1.1.2 (released 2019-11-18)

- Fixes werkzeug deprecation warning.

Version 1.1.1 (released 2018-12-26)

- Minimum version of Flask-Admin bumped to v1.5.3 due to Cross-Site Scripting
  vulnerability in previous versions.

Version 1.0.1 (released 2018-12-26)

- Minimum version of Flask-Admin bumped to v1.5.3 due to Cross-Site Scripting
  vulnerability in previous versions.

Version 1.1.0 (released 2018-12-14)

- Changed to using Webpack for static assets management instead of using
  AMD/RequireJS.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
