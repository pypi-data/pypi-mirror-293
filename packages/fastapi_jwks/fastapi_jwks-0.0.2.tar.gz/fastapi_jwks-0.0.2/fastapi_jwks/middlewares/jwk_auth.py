from fastapi import HTTPException
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from fastapi_jwks.validators import JWKSValidator


class JWKSAuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        jwks_validator: JWKSValidator,
        dispatch: DispatchFunction | None = None,
    ) -> None:
        super().__init__(app, dispatch)
        self.jwks_validator = jwks_validator

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        bearer_token = request.headers.get("authorization") or request.headers.get(
            "Authorization"
        )
        if not bearer_token or not bearer_token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token")
        token = bearer_token.removeprefix("Bearer ")
        request.state.payload = self.jwks_validator.validate_token(token)
        response = await call_next(request)
        return response
