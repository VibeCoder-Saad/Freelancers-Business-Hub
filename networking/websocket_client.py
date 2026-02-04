from PySide6.QtWebSockets import QWebSocket
from PySide6.QtCore import QUrl, QObject, Signal
import json

class WebSocketClient(QObject):
    message_received = Signal(dict) # Emits parsed JSON
    connected = Signal()
    disconnected = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.client = QWebSocket()
        self.client.connected.connect(self.on_connected)
        self.client.disconnected.connect(self.on_disconnected)
        self.client.textMessageReceived.connect(self.on_text_received)

    def connect_to_project(self, project_id):
        url = f"ws://localhost:8000/ws/project/{project_id}"
        self.client.open(QUrl(url))

    def on_connected(self):
        print("WebSocket Connected")
        self.connected.emit()

    def on_disconnected(self):
        print("WebSocket Disconnected")
        self.disconnected.emit()

    def on_text_received(self, message):
        try:
            data = json.loads(message)
            self.message_received.emit(data)
        except Exception as e:
            print(f"WS Parse Error: {e}")

    def close(self):
        self.client.close()
