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

    async def setup_hook(self):
        #---------
        # Add cogs
        #---------
        await self.load_extension("cogs.BaseCog")
        Utils.pront("Cogs loaded!")

    async def on_ready(self):
        # Command syncing
        Utils.pront("Syncing tree")
        await self.tree.sync()
        Utils.pront("Tree synced!")
        
        Utils.pront("Bot is ready", lvl="OKGREEN")

# Initialize bot object
bot = Bot()

# Custom error handler
async def on_tree_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):


    # Fallback default error
    await interaction.channel.send(
        embed=Utils.get_embed(interaction,
            title="An error occurred.",
            content=f'```ansi\n{error}```'
            )
        )
    # Allows entire error to be printed without raising an exception
    # (would create an infinite loop as it would be caught by this function)
    traceback.print_exc()
# Set error handler method
bot.tree.on_error = on_tree_error


# Ping command
@bot.tree.command(name="ping", description="Ping command")
async def _help(interaction: discord.Interaction) -> None:
    await Utils.send(interaction, 'Pong!')

bot.run(key)
