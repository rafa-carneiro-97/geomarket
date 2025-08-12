import jwt, datetime, logging
from django import http
from django.core.cache import cache
from django.conf import settings
from apps.users.models import User


def generate_jwt_token(request: http.HttpRequest, user: User):
    issued_at = datetime.datetime.now()
    expires_at = request.session.get_expiry_date()

    payload = {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
        "iat": issued_at,
        "exp": expires_at,
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def authenticate_jwt_header(request: http.HttpRequest) -> User | ValueError:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        logging.warning("JWT: token not found")
        raise ValueError("Unauthorized")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

    try:
        payload_user = _get_user(
            identifier=payload.get("id"),
            email=payload.get("email"),
            created_at=payload.get("created_at"),
        )
    except User.DoesNotExist:
        logging.warning("JWT: invalid payload user")
        raise ValueError("Invalid token")

    if request.user != payload_user:
        logging.warning(
            f'JWT: a user is trying to change the payloaded user. Request user: "{request.user.id}". Payload user: "{payload_user.id}".'
        )
        raise ValueError("Invalid token")

    return payload_user


def _get_user(
    identifier: int,
    email: str,
    created_at: str,
) -> User | ValueError:

    cache_key = f"user:{identifier}:{email}"
    user = cache.get(cache_key, None)

    if user is None:
        user = User.objects.get(
            id=identifier,
            email=email,
            created_at=created_at,
            is_active=True,
        )
        cache.set(cache_key, user, timeout=300)

    return user
