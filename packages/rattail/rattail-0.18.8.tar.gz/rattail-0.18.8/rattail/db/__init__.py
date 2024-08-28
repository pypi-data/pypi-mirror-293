# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Database Stuff
"""

import warnings

try:
    from .sess import Session, SessionBase as TrueSessionBase

except ImportError: # pragma: no cover
    Session = None
    SessionBase = None

else:

    class SessionBase(TrueSessionBase):

        def __init__(self, *args, **kwargs):
            warnings.warn("SessionBase should not be imported from rattail.db; "
                          "please import it from rattail.db.sess instead",
                          DeprecationWarning, stacklevel=2)
            super().__init__(*args, **kwargs)
