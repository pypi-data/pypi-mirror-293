from crypto_chassis_trade.utility.helper import create_url_with_query_params


class WebsocketConnection:
    def __init__(self, *, base_url=None, path=None, query_params=None, connection=None):
        self.base_url = base_url
        self.path = path
        self.query_params = query_params
        self.connection = connection
        self.latest_receive_message_time_point = None

    def as_pretty_dict(self):
        return {
            "base_url": self.base_url,
            "path": self.path,
            "query_params": self.query_params,
            "latest_receive_message_time_point": self.latest_receive_message_time_point,
        }

    @property
    def url_with_query_params(self):
        return create_url_with_query_params(base_url=self.base_url, path=self.path, query_params=self.query_params)
