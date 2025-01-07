import os
import discord
from discord import Intents, Object
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN")  # Your bot's token
GUILD_ID = 1325871678210965566  # Replace with your guild ID
ROLES_TO_REMOVE = [
    "⠀Айс - Отработка⠀",
    "⠀Дарина - Отработка⠀",
    "⠀Хан Максим - Отработка⠀",
    "⠀Нуржигит - Отработка⠀",
    "⠀Томирис - Отработка⠀",
    "⠀Карлыгаш - Отработка⠀",
    "⠀Айнура - Отработка⠀",
    "⠀Акбота - Отработка⠀",
    "⠀Ганибет - Отработка⠀",
    "⠀Жания - Отработка⠀",
    "⠀Айдар - Отработка⠀",
    "⠀Ермухаммет - Отработка⠀",
    "⠀Жолан - Отработка⠀",
    "⠀Алишер - Отработка⠀",
    "⠀Жибек - Отработка⠀",
    "⠀Тимофей - Отработка⠀",
    "⠀Асема - Отработка⠀",
    "⠀Елдос - Отработка⠀",
    "⠀Аружан - Отработка⠀",
    "⠀Бахтияр - Отработка⠀",
    "⠀Замирайлов Максим - Отработка⠀",
    "⠀Тахир - Отработка⠀",
]

# Bot setup
intents = Intents.default()
intents.guilds = True
intents.members = True  # Required for member operations
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Sync slash commands
    try:
        guild = Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild)
        print(f"Slash commands synced with guild ID {GUILD_ID}")
        
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# Slash command definition
@bot.tree.command(name="removeroles", description="Remove specific roles from all members")
async def removeroles(interaction: discord.Interaction):
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        await interaction.response.send_message("Guild not found.", ephemeral=True)
        return

    removed_count = 0
    failed_count = 0

    # Cache roles upfront for faster lookup
    role_cache = {
        role_name.strip().lower(): discord_role
        for role_name in ROLES_TO_REMOVE
        if (discord_role := discord.utils.get(guild.roles, name=role_name.strip()))
    }

    # Fetch all members
    await interaction.response.defer()  # Let the user know the bot is processing
    members = [member async for member in guild.fetch_members(limit=None)]

    # Remove roles
    for member in members:
        for role_name, role in role_cache.items():
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    removed_count += 1
                except Exception as e:
                    print(f"Failed to remove role '{role.name}' from {member.display_name}: {e}")
                    failed_count += 1

    await interaction.followup.send(
        f"Roles removed: {removed_count}\nFailures: {failed_count}"
    )


# Start the bot
bot.run(TOKEN)


