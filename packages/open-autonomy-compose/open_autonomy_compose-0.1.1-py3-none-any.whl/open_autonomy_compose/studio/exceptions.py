"""Exception classes."""


class ResourceException(Exception):
    """Base resource exceptio."""

    code: int


class BadRequest(ResourceException):
    """Bad request error."""

    code = 400


class ResourceAlreadyExists(ResourceException):
    """Bad request error."""

    code = 409


class NotFound(ResourceException):
    """Not found error."""

    code = 404


class NotAllowed(ResourceException):
    """Not allowed error."""

    code = 405
