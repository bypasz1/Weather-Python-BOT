import discord
from discord.ext import commands
import requests
import asyncio
import os  # Import necessário para usar 'os.system'

# Função para solicitar token e API key do usuário
def solicitar_credenciais():
    print("🚀 Inicializando o bot...")
    token = input("🔑 Insira o Token do bot Discord: ")
    api_key = input("🔑 Insira a API Key do WeatherAPI: ")

    # Limpa o terminal após o input
    if os.name == 'nt':  # Se for Windows
        os.system('cls')
    else:  # Se for Linux ou MacOS
        os.system('clear')

    # Aviso sobre possíveis erros
    print("\n⚠️ Atenção: Caso o token ou a chave da API estejam incorretos, o bot pode não funcionar corretamente.")
    return token, api_key

# Inicializa as credenciais
TOKEN, API_KEY = solicitar_credenciais()

# Configurações do bot
CHECK_INTERVAL = 3 * 60 * 60  # Intervalo de 3 horas

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Variáveis
alert_active = False
weather_task = None  # Variável para rastrear a tarefa de clima ativa
location = None  # Variável para armazenar a localização

def translate_condition(condition):
    translations = {
        "Clear": "☀️ Céu limpo",
        "Partly cloudy": "🌤️ Parcialmente nublado",
        "Cloudy": "☁️ Nublado",
        "Overcast": "🌥️ Encoberto",
        "Rain": "🌧️ Chuva",
        "Drizzle": "🌦️ Chuvisco",
        "Light rain": "🌧️ Chuva leve",
        "Thunderstorm": "⛈️ Tempestade",
        "Heavy rain": "🌧️🌧️ Chuva forte",
        "Snow": "❄️ Neve",
        "Fog": "🌫️ Nebuloso",
        "Mist": "🌁 Nevoeiro",
        "Dust": "🌪️ Poeira",
        "Sand": "🏜️ Areia",
        "Ash": "🌋 Cinzas",
        "Squall": "🌊 Ressaca",
        "Tornado": "🌪️ Tornado",
        "Sunny": "☀️ Ensolarado"
    }
    return translations.get(condition, condition)

async def fetch_weather(channel):
    global alert_active
    while alert_active:
        response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}')
        data = response.json()

        if "location" in data:
            current = data['current']
            location_info = data['location']
            time = location_info['localtime']
            date, hour = time.split()

            # Informações principais
            condition = translate_condition(current['condition']['text'])
            temp_c = current['temp_c']
            feels_like = current['feelslike_c']
            humidity = current['humidity']
            wind_speed = current['wind_kph']
            wind_dir = current['wind_dir']

            # Informações adicionais
            pressure = current['pressure_mb']
            cloud_cover = current['cloud']
            visibility = current['vis_km']
            uv_index = current['uv']
            gust_speed = current['gust_kph']

            # Mensagem formatada
            message = (f"**🌎 Clima em {location_info['name']}**\n"
                       f"📅 **Data:** {date}\n"
                       f"🕒 **Hora:** {hour}\n"
                       f"🌥️ **Condição:** {condition}\n"
                       f"🌡️ **Temperatura:** {temp_c}°C\n"
                       f"🤔 **Sensação Térmica:** {feels_like}°C\n"
                       f"💧 **Umidade:** {humidity}%\n"
                       f"🌬️ **Vento:** {wind_speed} km/h {wind_dir}\n\n"
                       f"🔍 **Informações adicionais:**\n"
                       f"🌀 **Rajadas de vento:** {gust_speed} km/h\n"
                       f"📊 **Pressão:** {pressure} hPa\n"
                       f"☁️ **Cobertura de nuvens:** {cloud_cover}%\n"
                       f"👁️ **Visibilidade:** {visibility} km\n"
                       f"🌞 **Índice UV:** {uv_index}\n")

            await channel.send(message)
        await asyncio.sleep(CHECK_INTERVAL)

@bot.command(name='start')
async def start_alert(ctx, *, user_location: str = None):
    global alert_active, weather_task
    if alert_active:
        await ctx.send("⚠️ O alerta de clima já está ativo.")
        return

    if user_location:
        global location
        location = user_location.capitalize()  # Formata a localização
    else:
        await ctx.send("🔍 Qual localização deseja? (Escreva na sua próxima mensagem, você tem 10 segundos)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for('message', timeout=10.0, check=check)
            location = msg.content.capitalize()  # Formata a localização
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo esgotado! Comando cancelado.")
            return

    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}')
    data = response.json()
    if "location" in data:
        city_name = data['location']['name']
        await ctx.send(f"📍 Localização definida para: {city_name}.")
        
        alert_active = True
        await ctx.send(f"🚨 Alerta de clima iniciado para: {city_name}. Você receberá atualizações a cada 3 horas.")

        # Inicia a tarefa de clima sem criar duplicatas
        if weather_task is None or weather_task.done():
            weather_task = asyncio.create_task(fetch_weather(ctx.channel))
    else:
        await ctx.send("❌ Cidade não encontrada. Tente novamente.")

@bot.command(name='stop')
async def stop_alert(ctx):
    global alert_active, weather_task
    if alert_active:
        alert_active = False
        await ctx.send("🛑 Alerta de clima parado.")
        
        if weather_task and not weather_task.done():
            weather_task.cancel()  # Cancela a tarefa de clima
            weather_task = None
    else:
        await ctx.send("❌ Não há nenhum alerta de clima ativo. Use `!start` para começar.")

@bot.command(name='status')
async def status_alert(ctx):
    if alert_active:
        await ctx.send("✅ O alerta de clima está ativo.")
    else:
        await ctx.send("❌ O alerta de clima está inativo.")

@bot.command(name='setlocation')
async def set_location(ctx, *, new_location: str):
    global location
    
    if not alert_active:
        await ctx.send("⚠️ O alerta de clima não está ativo. Use `!start` para ativar o alerta antes de definir a localização.")
        return

    location = new_location.capitalize()  # Formata a nova localização
    await ctx.send(f"📍 Localização definida para: {location}.")

@bot.command(name='ajuda')
async def help_command(ctx):
    help_message = (
        "❓ **Comandos disponíveis:**\n"
        "🔄 `!start <localização>` - Inicia o alerta de clima.\n"
        "⏹️ `!stop` - Para o alerta de clima.\n"
        "📝 `!status` - Verifica o status do alerta de clima.\n"
        "📍 `!setlocation <nova localização>` - Define uma nova localização.\n"
        "📜 `!credits` - Mostra informações de créditos.\n"
    )
    await ctx.send(help_message)

@bot.command(name='credits')
async def credits_command(ctx):
    credits_message = (
        "** ❕ Créditos:**\n\n"
        "👤 Este bot foi desenvolvido por [Pedro](https://www.instagram.com/p3dr0.012).\n\n"
        "❌ Não sou mais developer, fiz apenas pela didática, mas, se estiver interessado em saber sobre mim, me chama na dm do [insta](https://www.instagram.com/p3dr0.012) para trocarmos uma ideia!\n\n"
        "☁ Utiliza a API [WeatherAPI](https://www.weatherapi.com).\n\n"
        "📝 Observação: A API gratuita tem limitações e não temos orçamento, este projeto é completamente educacional e introdutório."
    )
    await ctx.send(credits_message)

# Inicia o bot
bot.run(TOKEN)
