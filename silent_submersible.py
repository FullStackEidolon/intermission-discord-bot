import os
import random
import logging
import asyncio
import requests
import discord
from datetime import datetime, timedelta
from typing import Optional

SCRYFALL_URL = "https://scryfall.com/card/war/66/silent-submersible"
CARD_IMAGE_PATH = "assets/silent_submersible.jpg"

SUB_MESSAGES = [
    "Periscope up.",
    "Silent but deadly.",
    "The sea is quiet tonight.",
    "Ready to breach.",
    "Submerged, not forgotten.",
    "Glub glub.",
    "It watches from below.",
    "The hull is strong, the will stronger.",
    "Running silent, running deep."
]

# Store the next post time globally for now
_next_post_time = None

def get_next_post_time() -> datetime | None:
    return _next_post_time

def set_next_post_time(dt: Optional[datetime]):
    global _next_post_time
    _next_post_time = dt

def time_until_next_post() -> str:
    if not _next_post_time:
        return "No post scheduled."
    delta = _next_post_time - datetime.utcnow()
    if delta.total_seconds() <= 0:
        return "Next post is imminent."
    minutes = int(delta.total_seconds() // 60)
    seconds = int(delta.total_seconds() % 60)
    return f"Next post in {minutes}m {seconds}s"

async def post_submersible_sdk(channel: discord.TextChannel, add_message=True, add_card=True):
    try:
        embed = discord.Embed(color=0x1f8b4c)

        if add_message:
            msg = random.choice(SUB_MESSAGES)
            embed.description = f"[{msg}]({SCRYFALL_URL})"

        if add_card and os.path.exists(CARD_IMAGE_PATH):
            file = discord.File(CARD_IMAGE_PATH, filename="silent_submersible.jpg")
            embed.set_image(url="attachment://silent_submersible.jpg")
            await channel.send(embed=embed, file=file)
        else:
            await channel.send(embed=embed)

    except Exception as e:
        logging.error(f"SDK post error: {e}")


def post_submersible_webhook(add_message=False, add_card=True, custom_avatar=True):
    webhook_url = os.getenv("SILENT_SUB_WEBHOOK")
    avatar_url = os.getenv("SUB_AVATAR_URL")

    if not webhook_url:
        logging.error("Webhook URL is missing.")
        return

    payload = {}
    files = {}

    if add_message:
        message = random.choice(SUB_MESSAGES)
        payload["content"] = f"[{message}]({SCRYFALL_URL})"

    if add_card and os.path.exists(CARD_IMAGE_PATH):
        files["file"] = open(CARD_IMAGE_PATH, "rb")

    if custom_avatar:
        payload["username"] = "Silent Submersible"
        payload["avatar_url"] = avatar_url

    try:
        response = requests.post(webhook_url, data=payload, files=files if files else None)
        if files:
            files["file"].close()

        if not response.ok:
            logging.error(f"Webhook post failed: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Exception during webhook post: {e}")
