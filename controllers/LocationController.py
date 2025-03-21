import socket
import os
import json

class LocationController:
    def __init__(self, locationService):
        self.SOCKET_PATH: str = '/tmp/sme-glcsvc.sock'
        self.locationService = locationService
        self.CONTEXT: str = 'GET_LOC'
        self.ALLOW_SOURCE: list[str] = ['CTL_LOCAL_SYS', 'CLT_CTRLR_SFT']
        self.ALLOW_VERSIONS: list[float] = [1.0]
        self._initSocket()

    def _initSocket(self):
        try:
            os.unlink(self.SOCKET_PATH)
        except OSError:
            if os.path.exists(self.SOCKET_PATH):
                raise RuntimeError(f"The socket file {self.SOCKET_PATH} already exists")

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.SOCKET_PATH)
        server.listen(5)
        print('Server is listening for incoming connections...')

        while True:
            try:
                connection, _ = server.accept()
                print("Client connected")
                data = connection.recv(1024)
                if data:
                    message: str = data.decode()
                    try:
                        message_dict = json.loads(message)

                        if 'source' not in message_dict or message_dict['source'] not in self.ALLOW_SOURCE:
                            self._sendJsonError(connection, "INVALID_SOURCE")
                            connection.close()
                            continue

                        if 'version' not in message_dict or message_dict['version'] not in self.ALLOW_VERSIONS:
                            self._sendJsonError(connection, "INVALID_VERSION")
                            connection.close()
                            continue

                        if 'request' not in message_dict or not isinstance(message_dict['request'], dict):
                            self._sendJsonError(connection, "INVALID_REQUEST_FORMAT")
                            connection.close()
                            continue

                        if 'type' not in message_dict['request'] or message_dict['request']['type'] != self.CONTEXT:
                            self._sendJsonError(connection, "UNKNOWN_CONTEXT")
                            connection.close()
                            continue

                        location = self.locationService.getLocation()
                        location_data = location.decode('utf-8') if isinstance(location, bytes) else location

                        response = {"location": location_data}
                        connection.sendall(json.dumps(response).encode('utf-8'))
                        connection.close()

                    except json.JSONDecodeError:
                        self._sendJsonError(connection, "INVALID_JSON_FORMAT")

                connection.close()

            except Exception as e:
                print(f"Error: {e}")
                connection.close()

    def _sendJsonError(self, connection: socket.socket, error_message: str) -> None:
        error_response = {
            "type": "error",
            "error": error_message
        }
        connection.sendall(json.dumps(error_response).encode('utf-8'))
