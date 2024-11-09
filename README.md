# Discord.py Example - Tutorial

Este é um bot para Discord desenvolvido com `discord.py` que oferece diversos comandos úteis, incluindo funcionalidades de administração, interação com usuários e status dinâmico.

## Funcionalidades

- **Comandos de Usuário:**
  - `.ajuda/help`: Mostra uma lista de comandos disponíveis.
  - `.ping`: Retorna a latência do bot.
  - `.rolar/roll (numero)`: Rola um dado com o número de lados especificado.
  - `.moeda/coin`: Realiza o sorteio de cara ou coroa.
  - `.warninfo (@user)`: Exibe o motivo e a quantidade de advertências de um usuário.

- **Comandos de Admin:**
  - `.say (mensagem)`: Faz o bot enviar uma mensagem personalizada.
  - `.ban (@user)`: Bane um usuário mencionado.
  - `.unban (id)`: Desbana um usuário por ID.
  - `.kick (@user)`: Expulsa um usuário mencionado.
  - `.clear (quantidade)`: Apaga uma quantidade de mensagens no chat.
  - `.mute (@user)`: Muta um usuário mencionado.
  - `.unmute (@user)`: Desmuta um usuário mencionado.
  - `.lock`: Trava o canal onde a mensagem foi enviada.
  - `.unlock`: Destrava o canal onde a mensagem foi enviada.
  - `.warn (@user)`: Aplica uma advertência a um usuário, que será banido após 3 advertências.
  - `.removewarn (@user)`: Remove a advertência de um usuário.
  - `.timeout (@user)`: Coloca um usuário em timeout (castigo).

## Tecnologias Utilizadas

- Python 3.x
- [discord.py](https://discordpy.readthedocs.io/en/stable/) para a criação do bot
- [asyncio](https://docs.python.org/3/library/asyncio.html) para a execução assíncrona
- [json](https://docs.python.org/3/library/json.html) para leitura e escrita de configurações

## Como Executar

1. Clone este repositório em sua máquina:
   ```bash
   git clone https://github.com/pedroosamp/discordpy-bot.git
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
4. Crie um arquivo config.json na raiz do projeto com o seguinte conteúdo:
   ```bash
   {
     "token": "SEU_TOKEN_AQUI",
     "prefix": "."
   }
5. Execute o bot:
   ```bash
   python bot.py
