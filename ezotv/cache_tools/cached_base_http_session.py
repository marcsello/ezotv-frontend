#!/usr/bin/env python3
import marshal
from requests_toolbelt.sessions import BaseUrlSession
from flask import current_app
from .redis_client import redis_client
from requests import Response
from requests.structures import CaseInsensitiveDict
from .cache_schema import CacheSchema
from marshmallow import ValidationError


class CachedResponse(Response):

    def __init__(self, content: bytes):
        super(CachedResponse, self).__init__()
        self._content = content

    @property
    def content(self):  # Overrides requests's internal content call
        return self._content


class CachedBaseHttpSession(BaseUrlSession):
    """
    The reason for the existance of this class is that requests-class does not support:
    - The flask redis client
    - using BaseUrlSession
    And I really don't want to monkey-patch it

    Marshal is used to store the response's contents instead of json,
    This is used because:
    - It serializes objects into bytes which could be save to redis without conversion
    - Easily serializes bytes type (the contents of a response)

    Marshmallow is used to validate the cached data, for basic protection against cache injection.
    """

    cache_schema = CacheSchema(many=False)

    def __init__(self, redis_cache_prefix: str, base_url=None):
        super().__init__(base_url)
        self._redis_cache_prefix = redis_cache_prefix

        self._default_cache_timeout = int(current_app.config['CACHE_TIMEOUT'])

    def get(self, url, cache_timeout=None, **kwargs) -> Response:

        cache_key = f"{self._redis_cache_prefix}_{url}"

        cached_data = redis_client.get(cache_key)

        data = None
        if cached_data:
            try:
                data = self.cache_schema.load(
                    marshal.loads(cached_data)
                )
            except (EOFError, ValueError, TypeError) as e:
                current_app.logger.error(f"Could not de-serialize cached response: {str(e)}")

            except ValidationError as e:
                current_app.logger.error(f"Could not validate cached response: {str(e)}")

        if data:
            current_app.logger.debug(f"Cache hit: {url} in {self._redis_cache_prefix}")

            response = CachedResponse(data['content'])
            response.status_code = data['status_code']
            response.headers = CaseInsensitiveDict(data['headers'])

        else:
            current_app.logger.debug(f"Cache miss: {url} in {self._redis_cache_prefix}")
            response = super().get(url, **kwargs)

            if response.status_code in [200, 204]:  # cache only successful responses
                data = {
                    'content': response.content,
                    'status_code': response.status_code,
                    'headers': dict(response.headers)
                }

                redis_client.set(cache_key, marshal.dumps(data))
                redis_client.expire(cache_key, cache_timeout or self._default_cache_timeout)

        return response
