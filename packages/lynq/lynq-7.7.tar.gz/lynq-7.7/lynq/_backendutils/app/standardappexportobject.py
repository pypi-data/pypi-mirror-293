from typing import Any

from lynq._backendutils.app.appobject import AppObject
from lynq._backendutils.app.app import app

class StandardAppExportObject:
    def __init__(self, app_: app, object_: Any = AppObject, *args: Any, **kwargs: Any) -> None:
        self.app: app = app_
        self.object: type[object_] = object_
        self.args: tuple[Any, ...] = args
        self.kwargs: dict[str, Any] = kwargs

    def launch(self) -> Any:
        app: type[self.object] = self.object(self.app.fn.__name__, self.app.server)
        try: return self.app.fn(app, *self.args, **self.kwargs)
        finally: app.pass_to_server()