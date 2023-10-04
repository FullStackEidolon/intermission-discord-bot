import os
import discord
from discord.ext import commands

# Set up Intents for the bot
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

# Create a new bot instance with a command prefix
bot_token = os.environ['BOT_TOKEN']
bot = commands.Bot(command_prefix='!', intents=intents)

# Lists to store movies and TV shows
MOVIES_FILE = 'data/movies.txt'
TV_SHOWS_FILE = 'data/tv_shows.txt'

def read_file(file_name):
    with open(file_name, 'a+') as f:  # 'a+' creates the file if it doesn't exist
        f.seek(0)  # Move the read cursor to the start of the file
        return [line.strip() for line in f.readlines()]


def append_to_file(file_name, content):
    with open(file_name, 'a') as f:
        f.write(content + '\n')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}({bot.user.id})')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def add_movie(ctx, *, movie_name: str):
    append_to_file(MOVIES_FILE, movie_name)
    await ctx.send(f'Movie "{movie_name}" added to the list!')

@bot.command()
async def add_tv(ctx, *, tv_show_name: str):
    append_to_file(TV_SHOWS_FILE, tv_show_name)
    await ctx.send(f'TV show "{tv_show_name}" added to the list!')

@bot.command()
async def list_movies(ctx):
    movies = read_file(MOVIES_FILE)
    response = "Movies:\n" + "\n".join(movies) if movies else "No movies added yet!"
    await ctx.send(response)

@bot.command()
async def list_tv(ctx):
    tv_shows = read_file(TV_SHOWS_FILE)
    response = "TV Shows:\n" + "\n".join(tv_shows) if tv_shows else "No TV shows added yet!"
    await ctx.send(response)

# Use your bot token to start the bot
bot.run(bot_token)
