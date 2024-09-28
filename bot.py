import discord
from discord.ext import commands, tasks
import requests
import asyncio

# Configurações do bot
TOKEN = 'token'  # Substitua pelo seu token
API_KEY = 'api'  # Substitua pela sua chave da API
CHECK_INTERVAL = 3 * 60 * 60  # Intervalo de 3 horas

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Variáveis
alert_active = False

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
        "Snow": "❄️ Neve",
        "Fog": "🌫️ Nebuloso",
        "Mist": "🌁 Nevoeiro",
        "Dust": "🌪️ Poeira",
        "Sand": "🏜️ Areia",
        "Ash": "🌋 Cinzas",
        "Squall": "🌊 Ressaca",
        "Tornado": "🌪️ Tornado"
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
            condition = translate_condition(current['condition']['text'])
            temp_c = current['temp_c']
            
            message = (f"**🌎 Clima em {location_info['name']}**\n"
                       f"📅 **Data:** {date}\n"
                       f"🕒 **Hora:** {hour}\n"
                       f"🌥️ **Condição:** {condition}\n"
                       f"🌡️ **Temperatura:** {temp_c}°C\n")
            
            await channel.send(message)
        await asyncio.sleep(CHECK_INTERVAL)

@bot.command(name='start')
async def start_alert(ctx, *, user_location: str = None):
    global alert_active
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
        await fetch_weather(ctx.channel)
    else:
        await ctx.send("❌ Cidade não encontrada. Tente novamente.")

@bot.command(name='stop')
async def stop_alert(ctx):
    global alert_active
    if alert_active:
        alert_active = False
        await ctx.send("🛑 Alerta de clima parado.")
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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user.mentioned_in(message):
        await message.channel.send("👋 Olá! Para ajuda, digite `!ajuda`.")

    await bot.process_commands(message)

# Inicia o bot
bot.run(TOKEN)
