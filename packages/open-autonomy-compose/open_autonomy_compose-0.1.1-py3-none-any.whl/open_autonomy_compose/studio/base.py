# pylint: disable=import-error, broad-except, no-self-use
"""Studio web view definitions."""

import typing as t
from abc import ABC, abstractmethod

from starlette.requests import Request  # type: ignore[import]
from starlette.responses import JSONResponse  # type: ignore[import]
from starlette.types import Receive, Scope, Send  # type: ignore[import]

from open_autonomy_compose.studio.exceptions import NotAllowed, ResourceException


GenericResource = t.TypeVar("GenericResource")
PostPayload = t.TypeVar("PostPayload")
PostResponse = t.TypeVar("PostResponse")
PutPayload = t.TypeVar("PutPayload")
PutResponse = t.TypeVar("PutResponse")
DeletePayload = t.TypeVar("DeletePayload")
DeleteResponse = t.TypeVar("DeleteResponse")


class Resource(
    t.Generic[
        GenericResource,
        PostPayload,
        PostResponse,
        PutPayload,
        PutResponse,
        DeletePayload,
        DeleteResponse,
    ],
    ABC,
):
    """Web<->Local resource object."""

    _handlers: t.Dict[str, t.Callable[[t.Dict], t.Dict]]

    def __init__(self) -> None:
        """Initialize object."""
        self._handlers = {
            "GET": self._get,  # type: ignore[dict-item]
            "POST": self._post,  # type: ignore[dict-item]
            "PUT": self._put,  # type: ignore[dict-item]
            "DELETE": self._delete,  # type: ignore[dict-item]
        }

    @property
    @abstractmethod
    def json(self) -> GenericResource:
        """Return JSON representation of the resource."""

    def create(self, data: PostPayload) -> PostResponse:
        """Create a new resource"""
        raise NotAllowed("Resource creation not allowed")

    def update(self, data: PutPayload) -> PostResponse:
        """Create a new resource"""
        raise NotAllowed("Resource update not allowed")

    def delete(self, data: DeletePayload) -> PostResponse:
        """Create a new resource"""
        raise NotAllowed("Resource deletion not allowed")

    def _get(self) -> GenericResource:
        """GET method for the resource."""
        return self.json

    def _post(self, data: PostPayload) -> PostResponse:
        """POST method for the resource."""
        return self.create(data=data)

    def _put(self, data: PutPayload) -> PutResponse:
        """PUT method for the resource."""
        return self.update(data=data)  # type: ignore[return-value]

    def _delete(self, data: DeletePayload) -> DeleteResponse:
        """DELETE method for the resource."""
        return self.delete(data=data)  # type: ignore[return-value]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> t.Any:
        """Web handler for sources."""
        request = Request(scope=scope, receive=receive, send=send)
        try:
            handler = self._handlers.get(request.method)
            if request.method == "GET":
                content = handler()  # type: ignore
            else:
                data = await request.json()
                content = handler(data)  # type: ignore[misc]
            response = JSONResponse(content=content)
        except ResourceException as e:
            response = JSONResponse(
                content={"error": e.args[0]},
                status_code=e.code,
            )
        except Exception as e:
            response = JSONResponse(
                content={"error": str(e)},
                status_code=500,
            )
        await response(scope=scope, receive=receive, send=send)
