import discord
from discord import app_commands, ui
from discord.ext import commands
import asyncio
import time
import re

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_cache = {}  # Cache de mensagens por usuário
        self.channel_cache = {}  # Cache de canais por usuário
        self.spam_threshold = 5  # Limite de mensagens em 5 segundos
        self.spam_interval = 5
        self.channel_threshold = 3  # Limite de canais diferentes em 5 segundos
        self.url_regex = r'https?://[^\s]+|discord\.gg/[^\s]+'  # Regex para URLs genéricas e invites

    def create_embed(self, title, description, color):
        return discord.Embed(title=title, description=description, color=color, timestamp=discord.utils.utcnow())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        current_time = time.time()

        # Inicializa caches do usuário
        if user_id not in self.message_cache:
            self.message_cache[user_id] = []
            self.channel_cache[user_id] = []

        self.message_cache[user_id].append(current_time)
        self.message_cache[user_id] = [t for t in self.message_cache[user_id] if current_time - t < self.spam_interval]
        if message.channel.id not in self.channel_cache[user_id]:
            self.channel_cache[user_id].append(message.channel.id)
        self.channel_cache[user_id] = [c for c in self.channel_cache[user_id] if current_time - self.message_cache[user_id][0] < self.spam_interval]

        # Verifica spam por mensagens
        config = await self.bot.db.get_config(message.guild.id)
        spam_limit = config.get("spam_limit", self.spam_threshold)
        spam_interval = config.get("spam_interval", self.spam_interval)

        if len(self.message_cache[user_id]) > spam_limit:
            await self.handle_spam(message, reason=f"Excesso de mensagens ({len(self.message_cache[user_id])} em {spam_interval}s)")
            return

        # Verifica flood em múltiplos canais
        if len(self.channel_cache[user_id]) >= self.channel_threshold:
            await self.handle_spam(message, reason=f"Flood em múltiplos canais ({len(self.channel_cache[user_id])} canais)", ban=True)
            return

        # Verifica URLs
        forbidden_links = config.get("forbidden_links", [])
        if re.search(self.url_regex, message.content.lower()) or any(link in message.content.lower() for link in forbidden_links):
            await self.handle_spam(message, reason="URL ou link proibido detectado")
            return

        # Aumenta reputação por mensagem válida
        await self.bot.db.update_reputation(user_id, message.guild.id, 1)
        await self.bot.process_commands(message)

    async def handle_spam(self, message, reason="Excesso de mensagens", ban=False):
        await message.delete()
        await message.author.send(embed=self.create_embed(
            title="🚨 Aviso de Spam",
            description=f"Você foi detectado enviando spam: {reason}. Seu comportamento foi registrado.",
            color=discord.Color.red()
        ))

        # Aplica mute ou ban
        if ban:
            try:
                await message.author.ban(reason=f"Spam detectado: {reason}")
                log_message = f"🚫 Usuário {message.author} banido por spam: {reason} (Canal: {message.channel.name}, Mensagem: {message.content})"
            except discord.Forbidden:
                log_message = f"❌ Falha ao banir {message.author}: Permissões insuficientes"
        else:
            mute_role = discord.utils.get(message.guild.roles, name="Muted")
            if not mute_role:
                mute_role = await message.guild.create_role(name="Muted", reason="Criação de cargo para mute")
                # Configura permissões do cargo Muted em todos os canais
                for channel in message.guild.channels:
                    await channel.set_permissions(mute_role, send_messages=False, add_reactions=False)
            
            await message.author.add_roles(mute_role)
            log_message = f"🔇 Usuário {message.author} mutado por spam: {reason} (Canal: {message.channel.name}, Mensagem: {message.content})"
            await asyncio.sleep(600)  # Remove mute após 10 minutos
            await message.author.remove_roles(mute_role)

        # Log da ação
        await self.log_action(message.guild, log_message)

    async def log_action(self, guild, message):
        config = await self.bot.db.get_config(guild.id)
        log_channel_id = config.get("log_channel")
        if log_channel_id:
            channel = guild.get_channel(int(log_channel_id))
            if channel:
                await channel.send(embed=self.create_embed(
                    title="📜 Log de Ação",
                    description=message,
                    color=discord.Color.orange()
                ))
        await self.bot.db.log_action(guild.id, message)

    class ConfigModal(ui.Modal, title="Configurar Regras de Spam"):
        messages = ui.TextInput(label="Limite de Mensagens", default="5")
        interval = ui.TextInput(label="Intervalo (segundos)", default="5")
        links = ui.TextInput(label="Links Proibidos (separados por vírgula)", required=False)

        async def on_submit(self, interaction: discord.Interaction):
            config = {
                "spam_limit": int(self.messages.value),
                "spam_interval": int(self.interval.value),
                "forbidden_links": [link.strip() for link in self.links.value.split(",") if link.strip()]
            }
            await interaction.client.db.update_config(interaction.guild.id, config)
            await interaction.response.send_message(embed=discord.Embed(
                title="✅ Configuração Atualizada",
                description=f"Limite: {self.messages.value} mensagens em {self.interval.value} segundos\nLinks proibidos: {', '.join(config['forbidden_links']) or 'Nenhum'}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ))

    @app_commands.command(name="config", description="Configura regras de spam")
    @app_commands.checks.has_permissions(administrator=True)
    async def config(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.ConfigModal())

    @app_commands.command(name="setlog", description="Define o canal de logs")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await self.bot.db.update_config(interaction.guild.id, {"log_channel": str(channel.id)})
        await interaction.response.send_message(embed=self.create_embed(
            title="✅ Canal de Logs Configurado",
            description=f"Logs serão enviados para {channel.mention}",
            color=discord.Color.green()
        ))

    @app_commands.command(name="stats", description="Exibe estatísticas do bot")
    async def stats(self, interaction: discord.Interaction):
        spam_count = await self.bot.db.get_spam_count(interaction.guild.id)
        config = await self.bot.db.get_config(interaction.guild.id)
        await interaction.response.send_message(embed=self.create_embed(
            title="📊 Estatísticas do Security Bot",
            description=f"**Spam detectado**: {spam_count}\n**Configurações ativas**: {len(config)}",
            color=discord.Color.blue()
        ))

    @app_commands.command(name="reputation", description="Verifica a reputação de um usuário")
    async def reputation(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        rep = await self.bot.db.get_reputation(user.id, interaction.guild.id)
        await interaction.response.send_message(embed=self.create_embed(
            title=f"🌟 Reputação de {user.name}",
            description=f"Pontuação: {rep.get('score', 0)}",
            color=discord.Color.blue()
        ))

async def setup(bot):
    await bot.add_cog(Security(bot))