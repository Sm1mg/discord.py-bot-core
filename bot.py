from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands
import subprocess
import random
import discord
import os

[4, 8, 15, 16, 23, 42]
print("Starting up...")

# Load .env
load_dotenv()
key = os.environ.get('key')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="%", intents=intents, case_insensitive=True)
bot.remove_command("help")

# Returns a random hexadecimal value from a given seed
async def getRandomHex(seed):
	random.seed(seed)
	return random.randint(0, 16777215)

# Creates a standard Embed object
async def getEmbed(ctx, title='', content='', footer=''):
	embed = discord.Embed(
		title=title,
		description=content,
		color=await getRandomHex(ctx.author.id)
	)
	embed.set_author(name=ctx.author.display_name,
					 icon_url=ctx.author.display_avatar.url)
	# embed.set_footer(footer=footer)
	return embed

# Creates and sends an Embed message
async def send(ctx, title='', content='', footer=''):
	embed = await getEmbed(ctx, title, content, footer)
	return await ctx.send(embed=embed)

# Print function
def pront(lvl, content):
	colors = {
		"LOG" : "",
		"OKBLUE" : "\033[94m",
		"OKCYAN" : "\033[96m",
		"OKGREEN" : "\033[92m",
		"WARNING" : "\033[93m",
		"ERROR" : "\033[91m",
		"NONE" : "\033[0m"
	}
	print(colors[lvl] + "{" + datetime.now().strftime("%x %X") + "} " + lvl + ": " + str(content) + colors["NONE"])

##
## Bot Events
##

# When bot connects to Discord
@bot.event
async def on_ready():
	pront('LOG', 'Bot Online!')

# Custom error handler
@bot.event
async def on_command_error(ctx, error):
	# If an unknown command is issued
	if isinstance(error, discord.ext.commands.errors.CommandNotFound):
		await send(ctx, 'Command not found:', f'{str(error)} is not a valid command, please refer to PREFIXHEREPREFIXHEREhelp for a list of commands.')
		return

	# If a command is on cooldown
	if isinstance(error, commands.CommandOnCooldown):
		await send(ctx, 'Command on cooldown:', f'This command is on cooldown, please try again in {round(error.retry_after)} seconds.')
		return


	pront("ERROR", str(error))
	# Send generic error message if none of the above apply
	await send(ctx, 'Oops!  Something just went wrong...', error)
	raise error

##
## Commands
##



##
## DEBUG/DEV COMMANDS
##

# Stop the bot
@bot.command(aliases=['pkys'])
@commands.is_owner()
async def phalt(ctx):
	await ctx.send("Halting bot, have fun dicking around with my code, asshole.")
	if ctx.author.voice is not None:
		await ctx.voice_client.disconnect()
	await ctx.bot.close()

# Evaluate a command sent by me
@bot.command(aliases=['peval'])
@commands.is_owner()
async def pexecute(ctx, *, arg):
	result = eval(arg)
	if result is not None:
		if len(result) >= 4000:
			split = [result[i:i+4000] for i in range(0, len(result), 4000)]
			for i in range(0, len(split)):
				await send(ctx, f"Eval result {i}/{len(split)-1}:", "```ascii\n"+split[i]+"\n```")
			return
		await send(ctx, "Eval result:", result)
		return
	await send(ctx, "Eval returned a NoneType.")

# Execute a shell command from discord (dangerous but whatever it's commands.is_owner())
@bot.command(aliases=['pcmd', 'prun', 'pshell'])
@commands.is_owner()
async def pcall(ctx, *, arg):
	result = subprocess.run(arg, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
	if len(result) >= 4000:
		split = [result[i:i+4000] for i in range(0, len(result), 4000)]
		for i in range(0, len(split)):
			await send(ctx, f"Result {i}/{len(split)-1}:", "```ascii\n"+split[i]+"\n```")
		return
	await send(ctx, f"Result:", "```ascii\n"+result+"\n```")

bot.run(key)
