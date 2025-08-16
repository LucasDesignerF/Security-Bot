import discord
from discord.ext import commands
import asyncio
import json
import os
from database.db import Database

# Configuração inicial do bot
with open("config.json", "r") as f:
    config_data = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Instância do banco de dados
db = Database(config_data["mongodb_uri"])

async def load_cogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"✅ Cog {filename} carregada com sucesso!")

@bot.event
async def on_ready():
    print(f"🚀 Bot conectado como {bot.user}")
    await bot.tree.sync()  # Sincroniza comandos slash
    bot.db = db  # Passa a instância do banco para o bot
    # Define uma atividade personalizada (status)
    activity = discord.CustomActivity(name="Protegendo o Tide Lab 🛡️")
    await bot.change_presence(activity=activity)
    print("🔄 Comandos slash sincronizados!")

async def main():
    await load_cogs()
    await bot.start(config_data["bot_token"])

if __name__ == "__main__":
    asyncio.run(main())