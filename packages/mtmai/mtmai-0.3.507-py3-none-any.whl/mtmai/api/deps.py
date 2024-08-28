from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from mtmai.core import security
from mtmai.core.config import settings
from mtmai.core.db import engine
from mtmai.core.queue import get_queue
from mtmai.models.models import TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False,  # 没有 token header 时不触发爆粗
)


# def get_token_from_cookie(request: Request) -> str | None:
#     # Get the token from the Authorization header or cookies
#     auth_header = request.headers.get("Authorization")
#     if auth_header and auth_header.startswith("Bearer "):
#         return auth_header.split(" ", 1)[1]  # Extract the token from the Bearer scheme

#     # Fallback to getting the token from the cookies
#     return request.cookies.get(settings.COOKIE_ACCESS_TOKEN)


# reusable_optional_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/login/access-token",
#     auto_error=False,  # 没有 token header 时不触发爆粗
# )


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_mq():
    queue = get_queue()
    yield queue


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
# OptionalTokenDep = Annotated[str, Depends(reusable_optional_oauth2)]
MqDep = Annotated[str, Depends(get_mq)]


def get_current_user(session: SessionDep, token: TokenDep, request: Request) -> User:
    token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_optional_current_user(
    session: SessionDep, token: TokenDep, request: Request
) -> User | None:
    token = token or request.cookies.get(settings.COOKIE_ACCESS_TOKEN)
    if not token:
        return None
    try:
        return get_current_user(session, token, request)
    except HTTPException:
        return None


OptionalUserDep = Annotated[User | None, Depends(get_optional_current_user)]
