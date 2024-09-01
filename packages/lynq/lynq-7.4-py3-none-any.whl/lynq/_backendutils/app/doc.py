from types import ModuleType
from importlib import import_module

from lynq._backendutils.app.app import app
from lynq._backendutils.server.standard import LynqServer

def generate_documentation(module_name: str, unique_port: int | None = None) -> None:
    module: ModuleType = import_module(module_name)

    @app(LynqServer(unique_port or 8000)) .export .standard
    def index(self) -> None:

        with self.head() as head:
            with head.title() as title:
                title.singular(f"Documentation for {module.__name__}")

            with head.style() as style:
                style.singular(r"body { font-family: arial; }")

        with self.body() as body:
            with body.h1() as h1:
                h1.singular(module.__name__)

            with body.h3() as h3:
                h3.singular(module.__file__)

            with body.p() as p:
                p.singular(module.__doc__)