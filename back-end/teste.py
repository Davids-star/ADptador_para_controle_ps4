import socket
import json

HOST = "192.168.18.82"  # ou seu IP
PORT = 5000         # mesma porta do .env

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# TESTE BOTÃO
data = {
    "type": "button",
    "button": "A",
    "pressed": True
}

client.send((json.dumps(data) + "\n").encode())

# SOLTAR
data["pressed"] = False
client.send((json.dumps(data) + "\n").encode())

client.close()