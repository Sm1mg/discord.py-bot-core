import discord
import os
import traceback
from discord.ext import commands
from dotenv import load_dotenv


# importing other classes from other files
import Utils

load_dotenv()  # getting the key from the .env file
key = os.environ.get('key')


class Bot(commands.Bot):  # initiates the bots intents and on_ready event
    def __init__(self):
        intents = discord.Intents.default()

        #-------------------
        # Set command prefix
        #-------------------
        super().__init__(command_prefix="​", intents=intents)
        self.synced=False

    async def on_ready(self):
        #---------
        # Add cogs
        #---------
        await bot.load_extension("cogs.BaseCog")
        Utils.pront("Cogs loaded!")

        #syncing tree
        Utils.pront("Syncing tree")
        if not self.synced:
            await bot.tree.sync()  # please dont remove just in case i need to sync
        Utils.pront("Tree synced!")

        #setting status
        Utils.pront("Setting bot status")
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"you in {len(bot.guilds):,} Servers."))
        
        Utils.pront("Bot is ready", lvl="OKGREEN")

# Global Variables
bot = Bot()

# Ping command
@bot.tree.command(name="ping", description="Ping command")
async def _help(interaction: discord.Interaction) -> None:
    await Utils.send(interaction, 'Pong!')

# Custom error handler
async def on_tree_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):


    # Fallback default error
    await interaction.channel.send(embed=Utils.get_embed(interaction, title="An error occurred.", content=f'```ansi\n{error}```', progress=False))
    # Allows entire error to be printed without raising an exception
    # (would create an infinite loop as it would be caught by this function)
    traceback.print_exc()
bot.tree.on_error = on_tree_error


bot.run(key)
