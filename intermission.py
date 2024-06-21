import os
import discord
import json
from discord.ext import commands
import logging
from dotenv import load_dotenv
import random

logging.basicConfig(level=logging.INFO)

# ENV Variablse
load_dotenv()

# Set up Intents for the bot
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

# Create a new bot instance with a command prefix
bot_token = os.environ['BOT_TOKEN']
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Lists to store movies and TV shows
MOVIES_FILE = 'data/movies.json'
TV_SHOWS_FILE = 'data/tv_shows.json'


def read_file(file_name):
    try:
        with open(file_name, 'r') as f:  # Open the file in read mode
            data = json.load(f)  # Load the list from the file
            logging.info(f"Data read from {file_name}: {data}")  # Debugging statement
            return data
    except (FileNotFoundError):  # If file doesn't exist or is empty
        logging.info(f"File not found or empty. Creating new list for {file_name}.")  # Debugging statement
        return []  # Return an empty list


def append_to_file(file_name, content):
    data = read_file(file_name)  # Read the existing data
    if content not in data:  # Check if the content is unique
        data.append(content)  # Append the new content
        logging.info(f"Appending {content} to {file_name}.")  # Debugging statement
    else:
        logging.info(f"{content} already in {file_name}, not adding.")  # Debugging statement
    with open(file_name, 'w') as f:  # Open the file in write mode
        json.dump(data, f)  # Write the updated list back to the file
        logging.info(f"Updated data written to {file_name}: {data}")  # Debugging statement


def delete_from_file(file_name, identifier):
    # Read the current items from the file
    items = read_file(file_name)
    deleted_item = None

    # First, try to interpret the identifier as an index
    if identifier.isdigit():
        index = int(identifier) - 1
        if 0 <= index < len(items):
            deleted_item = items.pop(index)
            logging.info(f"Deleted by index: {deleted_item}")
    else:
        # If not a valid index, try to find the item by substring match
        identifier_lower = identifier.lower()  # Convert once to avoid multiple conversions in the loop
        for item in items:
            if identifier_lower in item.lower():
                deleted_item = item
                items.remove(item)
                logging.info(f"Deleted by substring match: {deleted_item}")
                break

    # Write changes to file if an item was deleted
    if deleted_item:
        with open(file_name, 'w') as f:
            json.dump(items, f, indent=4)  # Optionally, consider pretty printing the JSON for readability
        return f'"{deleted_item}" removed from the list!'
    else:
        logging.info("No item found matching the given identifier.")
        return "Item not found. Please provide a valid index or substring."


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}({bot.user.id})')


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.command()
async def add_movie(ctx, *, movie_name):
    append_to_file(MOVIES_FILE, movie_name)
    await ctx.send(f'Movie "{movie_name}" added to the list!')


@bot.command()
async def add_tv(ctx, *, tv_show_name):
    append_to_file(TV_SHOWS_FILE, tv_show_name)
    await ctx.send(f'TV show "{tv_show_name}" added to the list!')


@bot.command()
async def list_movies(ctx):
    movies = read_file(MOVIES_FILE)
    if movies:
        response = "Movies:\n" + "\n".join(f"{index + 1}. {movie}" for index, movie in enumerate(movies))
    else:
        response = "No movies added yet!"
    await ctx.send(response)


@bot.command()
async def list_tv(ctx):
    tv_shows = read_file(TV_SHOWS_FILE)
    if tv_shows:
        response = "TV Shows:\n" + "\n".join(f"{index + 1}. {show}" for index, show in enumerate(tv_shows))
    else:
        response = "No TV shows added yet!"
    await ctx.send(response)


@bot.command()
async def delete_movie(ctx, *, identifier: str):
    response = delete_from_file(MOVIES_FILE, identifier)
    await ctx.send(response)


@bot.command()
async def delete_tv(ctx, *, identifier: str):
    response = delete_from_file(TV_SHOWS_FILE, identifier)
    await ctx.send(response)


@bot.command()
async def help(ctx, cmd: str = None):
    if cmd:
        cmd = cmd.lower()
        # Provide specific help for each command
        if cmd == 'hello':
            await ctx.send("Says hello! Usage: `!hello`")
        elif cmd == 'add_movie':
            await ctx.send("Adds a movie to the list. Usage: `!add_movie <movie_name>`")
        elif cmd == 'add_tv':
            await ctx.send("Adds a TV show to the list. Usage: `!add_tv <tv_show_name>`")
        elif cmd == 'list_movies':
            await ctx.send("Lists all the movies that have been added. Usage: `!list_movies`")
        elif cmd == 'list_tv':
            await ctx.send("Lists all the TV shows that have been added. Usage: `!list_tv`")
        elif cmd == 'delete_movie':
            await ctx.send(
                "Deletes a movie from the list based on its number or the name of the movie. Usage: `!delete_movie <number>`")
        elif cmd == 'delete_tv':
            await ctx.send(
                "Deletes a TV show from the list based on its number or the name of the tv show. Usage: `!delete_tv <number>`")
        else:
            await ctx.send(f"No detailed help available for '{cmd}'. Try `!help` for the list of commands.")
    else:
        help_text = """
Here are the commands you can use:

`!hello` - Says hello!

`!add_movie <movie_name>` - Adds a movie to the list. Replace `<movie_name>` with the name of the movie you want to add.

`!add_tv <tv_show_name>` - Adds a TV show to the list. Replace `<tv_show_name>` with the name of the TV show you want to add.

`!list_movies` - Lists all the movies that have been added.

`!list_tv` - Lists all the TV shows that have been added.

`!delete_movie <number>` - Deletes a movie from the list based on its name/number in the `!list_movies` command. Replace `<number>` with the number of the movie you want to remove.

`!delete_tv <number>` - Deletes a TV show from the list based on its name/number in the `!list_tv` command. Replace `<number>` with the number of the TV show you want to remove.

Type `!help command` for more info on a command.
"""
        await ctx.send(help_text)


@bot.command()
async def good_bot(ctx):
    emojis = [':smiley:', ':smile:', ':grin:', ':joy:', ':rofl:', ':laughing:', ':wink:']
    await ctx.send(random.choice(emojis))


@bot.command()
async def thats_a_good_pig(ctx):
    await ctx.send("Oink! :pig:")


@bot.command()
async def whos_dad(ctx):
    if ctx.author.name == "triskeilodon":
        await ctx.send("You!")
    else:
        uncertain_responses = [
            "ummm...", "hmmm...", "uhhh...", "errr...", "ahhh...",
            "mmm...", "ehhh...", "ooh...", "...dude..."
        ]
        await ctx.send(random.choice(uncertain_responses))


# Use your bot token to start the bot
bot.run(bot_token)
