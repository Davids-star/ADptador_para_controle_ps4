import asyncio
import websockets
from main import Controle
from dotenv import load_dotenv
import os
import signal
import sys
import psutil
sys.stdout.reconfigure(encoding='utf-8')

try:
    p = psutil.Process(os.getpid())
    if sys.platform == "win32":
        p.nice(psutil.HIGH_PRIORITY_CLASS)
except:
    pass

import http.server
import socketserver
import threading
import socket
import qrcode

load_dotenv()
controle = Controle()

# Força o servidor a escutar de todas as redes locais, e não apenas de um adaptador!
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT") or 5000)
WEB_PORT = 8080

def get_all_local_ips():
    ips = set()
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and not addr.address.startswith("127.") and not addr.address.startswith("169.254."):
                ips.add(addr.address)
    
    if not ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips.add(s.getsockname()[0])
            s.close()
        except:
            ips.add("127.0.0.1")
            
    return list(ips)

def start_web_server():
    local_ips = get_all_local_ips()
    
    print("\n" + "="*50)
    print("🌍 MÚLTIPLAS REDES DETECTADAS")
    print("Certifique-se de que o celular e o PC estão na mesma rede!")
    print("Tente escanear as opções abaixo:")
    print("="*50 + "\n")
    
    for ip in local_ips:
        url = f"http://{ip}:{WEB_PORT}"
        print(f"➜ NOVO QR CODE PARA O IP: {ip}")
        qr = qrcode.QRCode(version=1, box_size=1, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
        print(f"Acesso via URL: {url}\n")
        print("-" * 50)

    Handler = http.server.SimpleHTTPRequestHandler
    # Garante que a porta seja liberada rapidamente após o servidor ser encerrado
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    with ReusableTCPServer((HOST, WEB_PORT), Handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=start_web_server, daemon=True).start()

async def handler(websocket):
    client_ip = websocket.remote_address[0]
    print(f"[{client_ip}] Conectado ao app!")
    try:
        async for message in websocket:
            # Processar múltiplas mensagens se chegarem juntas
            for line in message.strip().split('\n'):
                if not line:
                    continue
                
                parts = line.split(',')
                msg_type = parts[0]

                # 🎮 BOTÃO
                if msg_type == "b":
                    button_name = parts[1]
                    pressed = parts[2] == '1'
                    print(f"[DEBUG] Botão {button_name} -> {'PRESSIONADO' if pressed else 'SOLTADO'}")

                    if button_name in controle.botoes:
                        if pressed:
                            controle.press_button(button_name)
                        else:
                            controle.release_button(button_name)
                    elif button_name in ("UP", "DOWN", "LEFT", "RIGHT"):
                        if pressed:
                            controle.move_setas(button_name)
                        else:
                            controle.release_setas(button_name)

                # 🕹️ JOYSTICK
                elif msg_type == "j":
                    x_int = int(max(-1, min(1, float(parts[2]))) * 32767)
                    y_int = int(max(-1, min(1, -float(parts[3]))) * 32767)
                    controle.move_joystick(x_int, y_int, 'left' if parts[1] == 'l' else 'right')

                # 🎯 GATILHO
                elif msg_type == "t":
                    controle.set_gatilhos(parts[1], int(max(0, min(1, float(parts[2]))) * 255))

            # ATUALIZA O ESTADO UMA ÚNICA VEZ APÓS LER AS MENSAGENS DESTE PACOTE
            controle.update()

    except websockets.exceptions.ConnectionClosed:
        print(f"[{client_ip}] Desconectado")
    except Exception as e:
        print("Erro:", e)

async def main():
    async with websockets.serve(handler, HOST, PORT):
        print("Servidor WebSocket rodando super rápido!")
        print(f"HOST: {HOST}")
        print(f"PORT: {PORT}")
        await asyncio.Future()  # roda pra sempre

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Servidor encerrado.")
