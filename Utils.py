import asyncio
import discord
import math
import random
import time
import yt_dlp.utils

from datetime import datetime


asyncio_tasks = set()

def pront(content, lvl="DEBUG", end="\n") -> None:
    """
    A custom logging method that acts as a wrapper for print().

    Parameters
    ----------
    content : `any`
        The value to print.
    lvl : `str`, optional
        The level to raise the value at.
        Accepted values and their respective colors are as follows:

        LOG : None
        DEBUG : Pink
        OKBLUE : Blue
        OKCYAN : Cyan
        OKGREEN : Green
        WARNING : Yellow
        ERROR : Red
        NONE : Resets ANSI color sequences
    end : `str` = `\\n` (optional)
        The character(s) to end the statement with, passes to print().
    """
    colors = {
        "LOG": "",
        "DEBUG": "\033[1;95m",
        "OKBLUE": "\033[94m",
        "OKCYAN": "\033[96m",
        "OKGREEN": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "NONE": "\033[0m"
    }
    # if type(content) != str and type(content) != int and type(content) != float:
    #    content = sep.join(content)
    print(colors[lvl] + "{" + datetime.now().strftime("%x %X") +
          "} " + lvl + ": " + str(content) + colors["NONE"], end=end)  # sep.join(list())


# Returns a random hex code
def get_random_hex(seed = None) -> int:
    """
    Returns a random hexidecimal color code.
    
    Parameters
    ----------
    seed : `int` | `float` | `str` | `bytes` | `bytearray` (optional)
        The seed to generate the color from.
        None or no argument seeds from current time or from an operating system specific randomness source if available.

    Returns
    -------
    `int`:
        The integer representing the hexidecimal code.
    """
    random.seed(seed)
    return random.randint(0, 16777215)


# Creates a standard Embed object
def get_embed(interaction, title='', content='', url=None, color='', progress: bool = True) -> discord.Embed:
    """
    Quick and easy method to create a discord.Embed that allows for easier keeping of a consistent style

    TODO change the content parameter to be named description to allow it to align easier with the standard discord.Embed() constructor.

    Parameters
    ----------
    interaction : `discord.Interaction`
        The Interaction to draw author information from.
    title : `str` (optional)
        The title of the embed. Can only be up to 256 characters.
    content : `str` (optional)
        The description of the embed. Can only be up to 4096 characters.
    url : `str` | `None` (optional)
        The URL of the embed.
    color : `int` (optional)
        The color of the embed.
    progress : `bool` = `True` (optional)
        Whether get_embed should try to automatically add the progress bar and now-playing information.

    Returns
    -------
    `discord.Embed`:
        The embed generated by the parameters.
    """
    if color == '':
        color = get_random_hex(interaction.user.id)
    embed = discord.Embed(
        title=title,
        description=content,
        url=url,
        color=color
    )
    embed.set_author(name=interaction.user.display_name,
                     icon_url=interaction.user.display_avatar.url)
    return embed


# Creates and sends an Embed message
async def send(interaction: discord.Interaction, title='', content='', url='', color='', ephemeral: bool = False, progress: bool = True) -> None:
    """
    A convenient method to send a get_embed generated by its parameters.

    Parameters
    ----------
    interaction : `discord.Interaction`
        The Interaction to draw author information from.
    title : `str` (optional)
        The title of the embed. Can only be up to 256 characters.
    content : `str` (optional)
        The description of the embed. Can only be up to 4096 characters.
    url : `str` | `None` (optional)
        The URL of the embed.
    color : `int` (optional)
        The color of the embed.
    progress : `bool` = `True` (optional)
        Whether get_embed should try to automatically add the progress bar and now-playing information.
    ephemeral : `bool` = `False` (optional)
    """
    embed = get_embed(interaction, title, content, url, color, progress)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)