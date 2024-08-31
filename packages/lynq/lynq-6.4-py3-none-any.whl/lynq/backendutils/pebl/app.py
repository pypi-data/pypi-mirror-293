"""
This file is part of Lynq (elemenom/lynq).

Lynq is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lynq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Your Package Name. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Optional
from typing import Callable

from lynq.backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq.launcher import launch

from lynq.backendutils.pebl.supportswith import SupportsWithKeyword
from lynq.backendutils.pebl.supportedtags import supported_tags

from lynq.backendutils.pebl.blankslateobject import new

class app(SupportsWithKeyword):
    def __init__(self, server: Optional[LynqServerOrRelatedObjects] = None) -> None:
        super().__init__()

        self.server: Optional[LynqServerOrRelatedObjects] = server

        self._init_root()

    def _init_root(self) -> None:
        self.export = new("export", (), # Export types here:
            standard = self._standard
        )

    def _standard(self, fn: Callable) -> Callable:
        self.fn: Callable = fn

        from lynq.backendutils.pebl.saeo import StandardAppExportObject

        return lambda *args, **kwargs: StandardAppExportObject(self, *args, **kwargs)