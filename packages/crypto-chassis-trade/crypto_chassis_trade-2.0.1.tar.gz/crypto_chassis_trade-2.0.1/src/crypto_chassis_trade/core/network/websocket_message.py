class WebsocketMessage:
    def __init__(
        self, *, websocket_connection=None, payload=None, json_deserialize=None, payload_summary=None, websocket_request_id=None, websocket_request=None
    ):
        self.websocket_connection = websocket_connection
        self.payload = payload
        self.json_deserialized_payload = json_deserialize(payload) if payload and json_deserialize else None
        self.payload_summary = payload_summary  # arbitrary dict containing parsed information (very specific for each exchange)
        self.websocket_request_id = websocket_request_id
        self.websocket_request = websocket_request

    def as_pretty_dict(self):
        return {
            "websocket_connection": self.websocket_connection.as_pretty_dict() if self.websocket_connection else None,
            "payload": self.payload,
            "json_deserialized_payload": self.json_deserialized_payload,
            "payload_summary": self.payload_summary,
            "websocket_request_id": self.websocket_request_id,
            "websocket_request": self.websocket_request.as_pretty_dict() if self.websocket_request else None,
        }
