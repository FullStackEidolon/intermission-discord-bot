# intermission-discord-bot
A discord bot written in Python to assist with server management and content requests

## Requirements:
WSL2 or Unix-based system
Docker
Docker Compose
Git

# Installation
1. Create a new bot at https://discord.com/developers/applications
2. Copy your bot token for later setup
3. Turn on appropriate presence permissions for the bot in the "Bot>Priviledged Gateway Intents" section
4. `cd` to the directory where you wish to install the bot
5. Run `git clone https://github.com/FullStackEidolon/intermission-discord-bot.git'
6. `cd intermission-discord-bot`
7. `echo "BOT_TOKEN=" > .env`
8. Add your bot token to the created .env file
9. `docker compose build`
10. `docker compose up -d`

Happy Sails!
