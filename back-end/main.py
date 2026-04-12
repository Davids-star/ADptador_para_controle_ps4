import vgamepad as vg
import sys
import json

class Controle:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()

        self.botoes = {
            "A": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
            "B": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
            "X": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            "Y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            "RB": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            "LB": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            "START": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
            "BACK": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            "L3": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
            "R3": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        }
        self.gatilhos_map =["LT", "RT"]

    def press_button(self, nome):
        if nome in self.botoes:
            self.gamepad.press_button(button=self.botoes[nome])

    def release_button(self, nome):
        if nome in self.botoes:
            self.gamepad.release_button(button=self.botoes[nome])

    def move_joystick(self, x_value, y_value, side="left"):
        if side == "left":
            self.gamepad.left_joystick(x_value=x_value, y_value=y_value)
        else:
            self.gamepad.right_joystick(x_value=x_value, y_value=y_value)
    
    def move_setas(self, direcao):
        mapa ={
            "UP": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            "DOWN": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            "LEFT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            "RIGHT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
        }
        if direcao in mapa:
            self.gamepad.press_button(button=mapa[direcao])

    
    def release_setas(self, direcao):
        for d in[
            vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
        ]:
        
            self.gamepad.release_button(button=d)

    def set_gatilhos(self, nome, valor):
        if nome == "LT":
            self.gamepad.left_trigger(value=valor)
        elif nome == "RT":
            self.gamepad.right_trigger(value=valor)

    def update(self):
        self.gamepad.update()

        
if __name__ == "__main__":
    controle = Controle()

    try:
        if sys.stdin.isatty():
            raise RuntimeError(
                "Este script espera JSON via stdin. Execute com pipe ou use back-end/serve.py para receber comandos."
            )

        raw = sys.stdin.readline()
        if not raw:
            raise EOFError("Nenhuma entrada recebida no stdin.")

        data = json.loads(raw)

        if data.get("type") == "button":
            nome = data["button"]

            if data["pressed"]:
                controle.press_button(nome)
            else:
                controle.release_button(nome)

        elif data["type"] == "joystick":
            def aplicar_deadzone(v, z=0.1):
                if abs(v) < z:
                    return 0
                return (v - z) / (1 - z) if v > 0 else (v + z) / (1 - z)
            
            x = aplicar_deadzone(data.get("x", 0))
            y = aplicar_deadzone(data.get("y", 0))

            # converter de -1..1 para -32768..32767
            x = int(max(-1, min(1, x)) * 32767)
            y = int(max(-1, min(1, y)) * 32767)

            controle.move_joystick(x, y)

        elif data["type"] == "trigger":
            nome = data["trigger"]
            valor = int(data["value"] * 255)

            controle.set_gatilhos(nome, valor)

    except Exception as e:
        print("Erro:", e)
