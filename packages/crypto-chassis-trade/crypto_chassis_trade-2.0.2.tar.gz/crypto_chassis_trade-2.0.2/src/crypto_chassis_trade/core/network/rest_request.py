import urllib.parse

from crypto_chassis_trade.utility.helper import (
    create_path_with_query_string,
    create_url,
)


class RestRequest:
    METHOD_GET = "GET"
    METHOD_HEAD = "HEAD"
    METHOD_POST = "POST"
    METHOD_PUT = "PUT"
    METHOD_DELETE = "DELETE"
    METHOD_CONNECT = "CONNECT"
    METHOD_OPTIONS = "OPTIONS"
    METHOD_TRACE = "TRACE"
    METHOD_PATCH = "PATCH"

    def __init__(
        self,
        *,
        id=None,
        base_url=None,
        method=None,
        path=None,
        query_params=None,
        query_string=None,
        payload=None,
        json_payload=None,
        json_serialize=None,
        headers=None,
        extra_data=None,
    ):
        self.id = id
        self.base_url = base_url
        self.method = method
        self.path = path
        self.query_params = query_params
        if query_params:
            self.query_string = "&".join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted(dict(query_params).items())])
        else:
            self.query_string = query_string
        self.headers = headers
        self.json_payload = json_payload
        if json_payload and json_serialize:
            self.payload = json_serialize(json_payload)
        else:
            self.payload = payload
        self.extra_data = extra_data

    def as_pretty_dict(self):
        return self.__dict__

    @property
    def url(self):
        return create_url(base_url=self.base_url, path=self.path)

    @property
    def path_with_query_string(self):
        return create_path_with_query_string(path=self.path, query_string=self.query_string)
