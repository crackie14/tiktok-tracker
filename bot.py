import discord
import tweepy
import asyncio

# ------------------ CONFIGURATION ------------------

# Clés API X (anciennement Twitter)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAKd5zgEAAAAAyS58OpoKMfYZTgy3%2BTKP0GOOSHc%3DdLW9UocBdqZxijMZAcKAFbJA5K5dIZjOmNDMpzyYe6JKMLFCwm"

# Token du bot Discord
DISCORD_TOKEN = "MTM0NDk1NzUzMTEwOTE5NTc4Nw.GGdOw9.NOhBvztTB7HBEFq8Wmm-4gOxnrT6_2yc6sHjOA"

# ID du canal Discord où envoyer les posts X
CHANNEL_ID = 1344964494186512424  # Remplace par l'ID du canal Discord

# Nom du compte X à suivre
X_USERNAME = "viraltoktracker"  # Remplace par le @ du compte à suivre

# ------------------ CONFIGURATION TERMINÉE ------------------

# Connexion à l’API X
client_x = tweepy.Client(bearer_token=BEARER_TOKEN)

# Connexion à l’API Discord
client_discord = discord.Client(intents=discord.Intents.default())


class XFeed:

    def __init__(self):
        self.last_post_id = None  # Stocke l’ID du dernier post envoyé

    async def fetch_latest_post(self):
        """Récupère le dernier post du compte X"""
        user = client_x.get_user(username=X_USERNAME)
        if not user.data:
            return None

        # Récupérer les posts récents
        posts = client_x.get_users_tweets(user.data.id, max_results=5)

        if posts.data:
            return posts.data[0]  # Retourne le dernier post

        return None


x_feed = XFeed()


async def check_posts():
    """Vérifie toutes les minutes s'il y a un nouveau post X"""
    await client_discord.wait_until_ready()
    channel = client_discord.get_channel(CHANNEL_ID)

    while not client_discord.is_closed():
        post = await x_feed.fetch_latest_post()

        if post and x_feed.last_post_id != post.id:
            x_feed.last_post_id = post.id
            post_url = f"https://fixupx.com/{X_USERNAME}/status/{post.id}"
            await channel.send(f"📢 Nouveau post X : {post.text}\n{post_url}")

        await asyncio.sleep(60)  # Vérifie toutes les 60 secondes


@client_discord.event
async def on_ready():
    print(f"Bot connecté en tant que {client_discord.user}")
    client_discord.loop.create_task(check_posts())


from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "Bot is running!"


def run():
    app.run(host='0.0.0.0', port=8080)


t = Thread(target=run)
t.start()

client_discord.run(DISCORD_TOKEN)
