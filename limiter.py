from slowapi import Limiter
from slowapi.util import get_remote_address
from config import settings

if settings.TESTING:
    limiter = Limiter(key_func=get_remote_address, enabled=not settings.TESTING)
else:
    limiter = Limiter(key_func=get_remote_address)