
# Weather Alert Discord Bot

Um bot simples para Discord que envia alertas climáticos a cada 3 horas, utilizando a [WeatherAPI](https://www.weatherapi.com). Você pode definir sua localização e receber atualizações sobre o tempo diretamente no seu servidor!

## 🚀 Funcionalidades

- **Alerta Climático**: Recebe alertas automáticos sobre o clima a cada 3 horas.
- **Localização Personalizada**: Defina a localização para receber as previsões.
- **Tradução de Condições Meteorológicas**: Condições climáticas traduzidas para facilitar o entendimento.
- **Respostas Inteligentes**: O bot responde quando mencionado, guiando os usuários para a ajuda disponível.
- **Comandos Simples**: Interface fácil para gerenciar os alertas.

## 📋 Pré-requisitos

- **Python 3.8+** instalado. [Baixe o Python aqui](https://www.python.org/downloads/).
- **WeatherAPI Key**: Cadastre-se em [WeatherAPI](https://www.weatherapi.com/signup.aspx) e obtenha sua chave de API gratuita.

## 🛠️ Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/bypasz1/Weather-Python-BOT.git
   ```

2. **Entre na pasta do projeto**:

   ```bash
   cd nome-do-repositorio
   ```

3. **Crie um ambiente virtual**:

   ```bash
   python -m venv venv
   ```

4. **Ative o ambiente virtual**:

   - No Windows:
     ```bash
     venv\Scripts\activate
     ```

   - No Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```

5. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Configure suas variáveis**:
   - No arquivo `bot.py`, substitua o valor de `TOKEN` pelo token do seu bot do Discord e o `API_KEY` pela sua chave da WeatherAPI.

7. **Execute o bot**:

   ```bash
   python bot.py
   ```

## 🚦 Comandos Disponíveis

Mencione o bot para começar ou siga a lista de comandos abaixo:

- `!start <localização>`: Inicia o alerta climático para a localização especificada.
- `!stop`: Para o alerta climático.
- `!status`: Verifica se o alerta está ativo ou inativo.
- `!setlocation <nova localização>`: Altera a localização para receber as atualizações de clima.
- `!ajuda`: Mostra os comandos disponíveis e suas funções.
- `!credits`: Exibe os créditos do projeto.

## 📝 Observações

- **Limitações da API**: A WeatherAPI na versão gratuita tem limitações de requisições, o que pode afetar o número de vezes que o bot consegue buscar atualizações.
- **Uso Educacional**: Este projeto é didático e não foi feito para fins comerciais.

## ❕ Créditos

👤 Este bot foi desenvolvido por [Pedro](https://www.instagram.com/p3dr0.012).

❌ Não sou mais developer, fiz apenas pela didática, mas, se estiver interessado em saber mais, me chama na DM do [insta](https://www.instagram.com/p3dr0.012) para trocarmos uma ideia!

☁ Utiliza a API [WeatherAPI](https://www.weatherapi.com).
