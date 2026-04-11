import asyncio
import websockets
from main import Controle
from dotenv import load_dotenv
import os
import signal
import sys

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

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_web_server():
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{WEB_PORT}"
    
    # Gera o QR Code Dinâmico no Terminal!
    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    
    print("\n" + "="*50)
    print(f"🌍 ACESSE A CAMERA DO CELULAR E ESCANEIE AQUI:")
    print("="*50 + "\n")
    qr.print_ascii(invert=True)
    print(f"\nOu acesse no navegador: {url}")
    print("="*50 + "\n")

    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((HOST, WEB_PORT), Handler) as httpd:
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
                if msg_type == "button":
                    try:
                        button_name = parts[1].strip()
                        pressed = parts[2].strip().lower() == 'true'

                        if button_name in controle.botoes:
                            if pressed:
                                print(f"🎮 Botão {button_name} APERTADO")
                                controle.press_button(button_name)
                                await websocket.send(f"Botão {button_name} pressionado")
                            else:
                                print(f"🎮 Botão {button_name} SOLTO")
                                controle.release_button(button_name)
                        elif button_name in ["UP", "DOWN", "LEFT", "RIGHT"]:
                            if pressed:
                                print(f"🕹️ Seta {button_name} APERTADA")
                                controle.move_setas(button_name)
                            else:
                                print(f"🕹️ Seta {button_name} SOLTA")
                                controle.release_setas(button_name)
                    except (ValueError, IndexError) as e:
                        print("Erro lendo botão:", e)


                # 🕹️ JOYSTICK
                elif msg_type == "joystick":
                    try:
                        side = parts[1].strip()
                        x = float(parts[2])
                        y = -float(parts[3])  # Eixo Y INVERTIDO
                        x_int = int(max(-1, min(1, x)) * 32767)
                        y_int = int(max(-1, min(1, y)) * 32767)
                        controle.move_joystick(x_int, y_int, side)
                        print(f"🕹️ Joystick {side.upper()} Movido: {x:.2f}, {y:.2f}")
                    except ValueError:
                        pass

                # 🎯 GATILHO
                elif msg_type == "trigger":
                    try:
                        trigger_name = parts[1].strip()
                        value = float(parts[2])
                        valor = int(max(0, min(1, value)) * 255)
                        controle.set_gatilhos(trigger_name, valor)
                        if value > 0:
                            print(f"🎯 Gatilho {trigger_name} PRESSIONADO ({valor})")
                        else:
                            print(f"🎯 Gatilho {trigger_name} SOLTO")
                    except (ValueError, IndexError):
                        pass

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
