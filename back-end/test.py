import socket

HOST = "192.168.18.82"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("🎮 Testador com feedback ativo")
print("Comandos: 'press BOTAO', 'release BOTAO', 'move X Y', 'trigger NOME VALOR', 'sair'")

while True:
    comando = input(">> ").strip().lower()

    if comando == "sair":
        break

    parts = comando.split()
    if len(parts) == 0:
        continue

    cmd = parts[0]
    if cmd == "press" and len(parts) == 2:
        botao = parts[1].upper()
        msg = f"button,{botao},true"
    elif cmd == "release" and len(parts) == 2:
        botao = parts[1].upper()
        msg = f"button,{botao},false"
    elif cmd == "move" and len(parts) == 3:
        try:
            x = float(parts[1])
            y = float(parts[2])
            msg = f"joystick,{x},{y}"
        except ValueError:
            print("❌ X e Y devem ser números")
            continue
    elif cmd == "trigger" and len(parts) == 3:
        nome = parts[1].upper()
        try:
            valor = float(parts[2])
            msg = f"trigger,{nome},{valor}"
        except ValueError:
            print("❌ Valor deve ser número")
            continue
    else:
        print("❌ Comando inválido. Use: press BOTAO, release BOTAO, move X Y, trigger NOME VALOR")
        continue

    client.send((msg + "\n").encode())

    # 🔥 espera resposta
    try:
        client.settimeout(2)
        resposta = client.recv(1024).decode().strip()
        print("📩 resposta:", resposta)
    except:
        print("⚠ sem resposta do servidor")

client.close()