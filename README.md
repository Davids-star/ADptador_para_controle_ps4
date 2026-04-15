# 🎮 PS4 Controller via Celular

Use seu **controle de PS4** conectado ao celular via Bluetooth para jogar no **PC**

---

## 📖 Como funciona

```
[Controle PS4] --Bluetooth--> [Celular] --Wi-Fi/USB Tethering--> [PC]
```

1. O controle de PS4 se conecta ao **celular via Bluetooth**
2. O celular acessa uma **página web** servida pelo PC
3. O navegador do celular lê os inputs do controle via [Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API)
4. Os dados são enviados em tempo real para o PC via **WebSocket**
5. O PC recebe os dados e simula um **controle virtual Xbox** (usando `vgamepad`)
6. O jogo no PC detecta o controle como se fosse um gamepad físico conectado

---

## 🗂️ Estrutura do Projeto

```
ps4/
├── back-end/
│   ├── serve.py       # Servidor WebSocket + servidor HTTP (serve o index.html)
│   ├── main.py        # Classe Controle — simula o gamepad virtual no PC
│   └── index.html     # Interface web aberta no celular (capta inputs via Gamepad API)
├── requirements.txt   # Dependências Python
├── iniciar.bat        # Script para iniciar o servidor no Windows
└── .env               # Configurações de porta (opcional)
```

---

## ⚙️ Pré-requisitos

- **Windows 10/11** (necessário para o driver `vgamepad`)
- **Python 3.10+**
- **ViGEmBus Driver** instalado → [Download aqui](https://github.com/nefarius/ViGEmBus/releases)
- Um celular com **Chrome ou Edge** (suporte à Gamepad API)
- Controle de PS4

---

## 🚀 Como usar

### 1. Instale o ViGEmBus
Baixe e instale o driver em: https://github.com/nefarius/ViGEmBus/releases

### 2. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 3. Inicie o servidor
Dê dois cliques em **`iniciar.bat`** ou rode no terminal:
```bash
iniciar.bat
```
O script vai:
- Ativar o ambiente virtual (`.venv`)
- Instalar as dependências automaticamente
- Iniciar o servidor

### 4. Conecte o celular
Após iniciar, o terminal vai exibir **QR Codes** para cada rede disponível.

- Escaneie o QR Code com o celular
- Certifique-se de que PC e celular estão **na mesma rede Wi-Fi**
  > 💡 Você também pode usar **USB Tethering** para conexão mais rápida e sem latência!

### 5. Conecte o controle PS4 no celular
- Ative o Bluetooth no celular
- Ligue o PS4, segure **PS + Share** até a luz piscar
- Pareie com o celular

### 6. Abra a página no celular e jogue!
Toque na tela após conectar o controle. O status deve mudar para:
> ✅ **CONTROLE ATIVO E ENVIANDO SINAIS!**

---

## 🌐 Portas utilizadas

| Porta | Uso |
|-------|-----|
| `8080` | Servidor HTTP (página web para o celular) |
| `5000` | Servidor WebSocket (comunicação em tempo real) |

---

## 📦 Dependências Python

| Pacote | Uso |
|--------|-----|
| `vgamepad` | Simula um controle virtual Xbox no Windows |
| `websockets` | Servidor WebSocket assíncrono |
| `psutil` | Detecta IPs locais e ajusta prioridade do processo |
| `qrcode` | Gera QR Codes no terminal para facilitar o acesso |
| `python-dotenv` | Lê variáveis do arquivo `.env` |
| `Pillow` | Dependência do qrcode |

---

## 🔧 Configuração opcional (`.env`)

```env
PORT=5000
```

---

## ⚡ Dica de performance — USB Tethering

Para menor latência, use **USB Tethering** em vez de Wi-Fi:

1. Conecte o celular ao PC via cabo USB
2. No Android: **Configurações → Rede → Hotspot → Tethering USB**
3. Rode o servidor normalmente — ele detecta todas as interfaces automaticamente

---

## 🛠️ Tecnologias

- **Python** — Backend / servidor
- **WebSockets** — Comunicação em tempo real
- **Gamepad API** — Leitura do controle no navegador mobile
- **vgamepad + ViGEmBus** — Emulação de gamepad virtual no Windows
- **HTML/CSS/JS** — Interface web no celular

---

## 📄 Licença

MIT — Fique à vontade para usar, modificar e contribuir!
