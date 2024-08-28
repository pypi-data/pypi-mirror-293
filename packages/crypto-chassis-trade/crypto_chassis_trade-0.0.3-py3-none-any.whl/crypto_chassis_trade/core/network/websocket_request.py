class WebsocketRequest:
    def __init__(self, *, id=None, payload=None, json_payload=None, json_serialize=None, extra_data=None):
        self.id = id
        self.json_payload = json_payload
        if json_payload and json_serialize:
            self.payload = json_serialize(json_payload)
        else:
            self.payload = payload
        self.extra_data = extra_data

    def as_pretty_dict(self):
        return self.__dict__
