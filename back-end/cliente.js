
const net = require("net");
require("dotenv").config();

const HOST = process.env.HOST;
const PORT = process.env.PORT;
const client = new net.Socket();

function enviar(comando) {
    client.write(comando);
}

client.connect(PORT, HOST, () => {
  console.log("Conectado ao servidor");

// TESTE
  enviar("press A");

  setTimeout(() => enviar("release A"), 500);

  setTimeout(() => enviar("move 100 -100"), 1000);

  setTimeout(() => enviar("set LT 255"), 1500);
  
  setInterval(() => {
    enviar("move 0 32767");
  }, 100);

});

function segurar(botao, tempo = 500) {
  enviar(`press ${botao}`);

  setTimeout(() => {
    enviar(`release ${botao}`);
  }, tempo);
}

// exemplo
segurar("A", 1000);

setInterval(() => {
  enviar("move 0 32767"); // pra frente
}, 100);

const controle = {
  frente: () => enviar("move 0 32767"),
  tras: () => enviar("move 0 -32767"),
  direita: () => enviar("move 32767 0"),
  esquerda: () => enviar("move -32767 0"),

  pular: () => segurar("A", 200),
};
