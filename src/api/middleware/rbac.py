from collections.abc import Callable

from fastapi import HTTPException, Request, Response


async def require_role(request: Request, call_next: Callable[[Request], Response]) -> Response:
    if request.url.path.startswith("/api/admin") and request.headers.get("x-role") != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    return await call_next(request)
