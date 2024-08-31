from typing import Callable
from typing import Any

from lynq.backendutils.pebl.appobject import AppObject
from lynq.app import app

class StandardAppExportObject:
    def __init__(self, app: app, *args: Any, **kwargs: Any) -> None:
        self.app: app = app
        self.args: tuple[Any, ...] = args
        self.kwargs: dict[str, Any] = kwargs

    def launch(self) -> Any:
        app: AppObject = AppObject(self.app.fn.__name__, self.app.server)
        try: return self.app.fn(app, *self.args, **self.kwargs)
        finally: app.pass_to_server()