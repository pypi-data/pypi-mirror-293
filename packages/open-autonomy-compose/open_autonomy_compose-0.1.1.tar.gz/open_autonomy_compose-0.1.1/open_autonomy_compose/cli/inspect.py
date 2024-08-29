# pylint: disable=import-error, unused-argument, no-self-use
"""Start an inspect server."""

import asyncio
import webbrowser
from pathlib import Path

from clea import Boolean, Directory, Integer, String  # type: ignore[import]
from starlette.applications import Starlette  # type: ignore[import]
from starlette.middleware import Middleware  # type: ignore[import]
from starlette.middleware.cors import CORSMiddleware  # type: ignore[import]
from starlette.requests import Request  # type: ignore[import]
from starlette.responses import HTMLResponse, JSONResponse  # type: ignore[import]
from starlette.routing import Mount, Route  # type: ignore[import]
from starlette.staticfiles import StaticFiles  # type: ignore[import]
from typing_extensions import Annotated
from uvicorn.main import run as uvicorn  # type: ignore[import]

from open_autonomy_compose.cli import compose
from open_autonomy_compose.data import DATA_DIR
from open_autonomy_compose.fsm.composition import Composition, CompositionSpecification
from open_autonomy_compose.helpers.package import load_packages


class Inspect:
    """View-Controller for inspect tool."""

    def __init__(self, app: Path) -> None:
        """Initialize object."""
        self._app = app

    def spec(self) -> CompositionSpecification:
        """Load FSM spec."""
        asyncio.set_event_loop(asyncio.new_event_loop())  # Patch for AEA multiplexer
        load_packages(self._app.parent.parent.parent)
        return CompositionSpecification.from_obj(
            composition=Composition.from_path(
                path=self._app,
            ),
        )

    def index(self, request: Request) -> HTMLResponse:
        """Index page."""
        return HTMLResponse(
            content=(DATA_DIR / "site" / "index.html").read_text(encoding="utf-8")
        )

    def get_fsm(self, request: Request) -> JSONResponse:
        """Returns FSM as json."""
        return JSONResponse(
            content=self.spec().to_json(),  # type: ignore[call-arg]
        )


@compose.command
def inspect(
    app: Annotated[Path, Directory(exists=True, resolve=True)],
    browser: Annotated[bool, Boolean()],
    host: Annotated[str, String()] = "localhost",
    port: Annotated[int, Integer()] = 8000,
) -> None:
    """Inspect a ABCI app composition in a webview."""

    def _on_startup() -> None:
        """On startup."""
        if browser:
            webbrowser.open(url=f"http://{host}:{port}")

    ivc = Inspect(
        app=app,
    )
    uvicorn(
        app=Starlette(
            debug=True,
            routes=[
                Route("/", ivc.index),
                Route("/fsm", ivc.get_fsm),
                Mount(
                    "/_next",
                    app=StaticFiles(directory=DATA_DIR / "site" / "_next"),
                    name="static",
                ),
            ],
            middleware=[Middleware(CORSMiddleware, allow_origins=["*"])],
            on_startup=[_on_startup],
        ),
        host=host,
        port=port,
    )
