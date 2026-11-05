from anthropic import Anthropic

from app.core.config import settings

client = Anthropic(
    api_key=settings.anthropic_api_key,
    max_retries=2,   # retries rate limits and temporary server errors
    timeout=60.0,    # seconds
)