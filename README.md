# Weather Python Discord BOT

## Descrição

O **Weather Python Discord BOT** é um bot para Discord que fornece atualizações sobre as condições climáticas em tempo real usando a API WeatherAPI. O bot permite que os usuários configurem alertas de clima para uma localização específica, com notificações a cada 3 horas.

## Funcionalidades

- Iniciar alertas de clima com o comando `!start <localização>`.
- Parar alertas de clima com o comando `!stop`.
- Verificar o status do alerta de clima com `!status`.
- Alterar a localização do alerta com `!setlocation <nova localização>`.
- Receber uma lista de comandos disponíveis com `!ajuda`.
- Obter informações de créditos com `!credits`.

## Como Configurar

1. **Pré-requisitos:**
   - Python 3.7 ou superior.
   - Bibliotecas necessárias:
     ```bash
     pip install discord.py requests
     ```

2. **Obter Credenciais:**
   - Crie um bot no [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications).
   - Copie o Token do bot.
   - Crie uma conta na [WeatherAPI](https://www.weatherapi.com/) e obtenha sua API Key.

3. **Configuração do Bot:**
   - Clone este repositório:
     ```bash
     git clone <https://github.com/bypasz1/Weather-Python-BOT>
     ```
   - Navegue até o diretório do bot:
     ```bash
     cd <C:\Users\User\Desktop\Weather-Python-BOT>
     ```
   - Execute o bot:
     ```bash
     python bot.py
     ```

4. **Inserir Credenciais:**
   - Ao iniciar o bot, você será solicitado a inserir o Token do Discord e a API Key do WeatherAPI.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar um pull request ou abrir uma issue para discutir melhorias.

## Licença

Este projeto é licenciado sob a MIT License - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
