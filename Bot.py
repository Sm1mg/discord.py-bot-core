import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


# importing other classes from other files
import Utils

load_dotenv()  # getting the key from the .env file
key = os.environ.get('key')

class Bot(commands.Bot):  # initiates the bots intents and on_ready event
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        #-----------
        # Add prefix
        #-----------
        super().__init__(intents=intents, command_prefix="TODO")


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

    async def on_command_error(self, ctx: commands.Context, exception: commands.CommandError) -> None:

        
        # Fallback default error
        await ctx.channel.send(
            embed=Utils.get_embed(ctx,
                title="An error occurred.",
                description=f'```ansi\n{exception}```'
            )
        )

# Initialize bot object
bot = Bot()


# Ping command
@bot.hybrid_command(name="ping", with_app_command = True, description="Ping command")
async def _ping(ctx: commands.Context) -> None:
    await Utils.send(ctx, 'Pong!')

bot.run(key)
