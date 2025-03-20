import socket
import os
import json

class LocationController:
    def __init__(self, locationService):
        self.SOCKET_PATH: str = '/tmp/smx-glc-service.sock'
        self.locationService = locationService
        self.CONTEXT: str = 'GET_LOCATION'
        self._initSocket()

    def _initSocket(self):
        try:
            os.unlink(self.SOCKET_PATH)
        except OSError:
            if os.path.exists(self.SOCKET_PATH):
                raise RuntimeError(f"The socket file {self.SOCKET_PATH} is already exist")

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
                        if 'type' in message_dict:
                            if message_dict['type'] == self.CONTEXT:
                                location = self.locationService.getLocation()
                                connection.sendall(location)
                            else:
                                self._sendJsonError(connection,"UNKNOWN_CONTEXT")
                        else:
                            self._sendJsonError(connection,"UNEXPECTED_FORMAT")

                    except json.JSONDecodeError:
                         self._sendJsonError(connection,"INVALID_JSON_FORMAT")
                         connection.close()

            except Exception as e:
                print(f"Error: {e}")
                connection.close()

    def _sendJsonError(self, connection: socket, error_message: str) -> None:
            error_response = {
                "type": "error",
                "error": error_message
            }
            connection.sendall(json.dumps(error_response).encode('utf-8'))
