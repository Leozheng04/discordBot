import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import asyncio
import yt_dlp


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
handler.setFormatter(formatter)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

voice_clients = {}
yt_dl_options = {
    "format": "bestaudio/best",
    "noplaylist": True,       # don’t download full playlists
    "quiet": True,            # suppress output
    "nocheckcertificate": True,
    "ignoreerrors": True,
    "no_warnings": True,
    "default_search": "ytsearch",  # allows using keywords
    "source_address": "0.0.0.0"    # prevents IPv6 issues
}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {'options':'-vn'}

#event section
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_member_join(member):
     channel = discord.utils.get(member.guild.text_channels, name="general")
     if channel: 
        await channel.send(f"{member.mention} has descended upon our server!")

@bot.event
async def on_member_remove(member):
     channel = discord.utils.get(member.guild.text_channels, name="general")
     if channel: 
        await channel.send(f"{member.mention} is no longer with us :(!)")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if "raymon" in content:
        await message.channel.send("Raymon is in the bathroom.")
    elif "aaron" in content:
        await message.channel.send("Eren Yeager?")
        await message.channel.send("https://tenor.com/view/attack-on-titan-eren-yeager-eren-jaeger-fortnite-griddy-eren-hitting-that-griddy-no-way-gif-27684348")
    elif "carmen wong" in content:
        await message.channel.send("Wong stand for Won Ton Soup")
        await message.channel.send("https://tenor.com/view/wonton-soup-gif-9902358")
    elif "leo" in content:
        await message.channel.send("How dare you call out thy name")

    await bot.process_commands(message)

#Social Commands

@bot.command()
async def eightball(ctx):
    fate = ["No","Yes", "Maybe","Hell Nah","Not in a Million Years!", "Yessir", "Definitely", 
            "Most likely","No means No!","I Doubt it","Sure","Signs point to Yes", "Certainly"]
    choice = random.choice(fate)
    await ctx.channel.send(choice)

@bot.command()
async def rolldice(ctx):
    choice = random.randint(1,6)
    await ctx.channel.send(f"🎲 You just rolled a {choice} !")

@bot.command()
async def roast(ctx, member: discord.Member):
    target =  member or ctx.author
    roasts = [
    f"Holy moly, {target.mention}'s forehead is so big it starts reflecting sunlight.",
    f"{target.mention} is so chopped that when they were catcalling, the police arrested them for harassment.",
    f"{target.mention} is so broke they started using socks as gloves for the winter.",
    f"When {target.mention} asked the magic mirror in Snow White for confirmation, it shattered and declared them the ugliest person within a thousand kilometers.",
    f"{target.mention} went to Hogwarts and got sorted into the trash bin.",
    f"{target.mention} asked the genie for three wishes, and the genie wished *them* away.",
    f"{target.mention} is so ugly that when they play peekaboo, people call 911.",
    f"{target.mention}, you’re like a pop-up ad — unwanted, loud, and impossible to close.",
    f"{target.mention}, your brain has buffering issues — please reconnect to reality.",
    f"{target.mention} radiates 'rizzless NPC energy.'",
    f"{target.mention} got their personality from comment sections.",
    f"{target.mention}, you look like you unironically say 'Sigma Skibidi Ohio Rizzler' in job interviews.",
    f"{target.mention} got folded by a cameraman in episode 12 and still hasn’t respawned.",
    f"{target.mention} makes onions cry out of respect.",
    f"{target.mention}, you smell like expired confidence and burnt toast."
    ]

    choice = random.choice(roasts)
    await ctx.channel.send(choice)

@bot.command()
async def hug(ctx,member: discord.Member):
    target = member or ctx.author
    actions =[
    f"{ctx.author.mention} gives {target.mention} a big warm hug 🤗",
    f"{ctx.author.mention} wraps {target.mention} up in a cozy embrace 💞",
    f"{ctx.author.mention} gives {target.mention} a surprise hug from behind 👀💗"
    ]
    choice = random.choice(actions)

    gif =[
        "https://tenor.com/view/enage-kiss-anime-hug-kisara-gif-26118528",
        "https://tenor.com/view/anime-hug-gif-26637494",
        "https://tenor.com/view/scarlie-gif-9252297952066858510",
        "https://tenor.com/view/ily-ilysm-silly-gif-16781489622612968569",
        "https://tenor.com/view/casal-anime-anime-triste-abra%C3%A7o-gif-1816195125907342270",
        "https://tenor.com/view/hug-happy-hugging-friends-cute-gif-7898446808540296103",
        "https://tenor.com/view/anki-blt-gif-3824273406997845560",
        "https://tenor.com/view/bot-gif-4033636017272611761",
        "https://tenor.com/view/cute-anime-hug-gif-5188990491482568848",
        "https://tenor.com/view/anime-hug-hug-hugs-anime-girl-hug-anime-girl-hugging-boy-gif-26094818",
        "https://tenor.com/view/gay-glomp-anime-bromance-gay-anime-gif-27667730",
        "https://tenor.com/view/pjsk-pjsk-anime-project-sekai-project-sekai-anime-mmj-gif-5674854375745473708"
    ]
    gif_choice = random.choice(gif)
    await ctx.channel.send(choice)
    await ctx.channel.send(gif_choice)

#music bot 
@bot.command(name='play')
async def play(ctx, url: str):
    try:
        if ctx.author.voice is None:
            await ctx.send("You're not connected to a voice channel!")
            return

        # Connect to voice if not already connected
        if ctx.guild.id not in voice_clients or not voice_clients[ctx.guild.id].is_connected():
            voice_client = await ctx.author.voice.channel.connect()
            voice_clients[ctx.guild.id] = voice_client
        else:
            voice_client = voice_clients[ctx.guild.id]

        # Extract audio stream
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        song = data['url']

        # Create audio source and play
        player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
        voice_client.play(player)

        await ctx.send(f"🎶 Now playing: {data.get('title', 'Unknown title')}")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        print(e)

@bot.command(name='pause')
async def pause(ctx):
    try:
        voice_clients[ctx.guild.id].pause()
        await ctx.send("⏸️ Paused playback.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        print(e)

@bot.command(name='resume')
async def resume(ctx):
    try:
        voice_clients[ctx.guild.id].resume()
        await ctx.send("▶️ Resumed playback.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        print(e)

@bot.command(name='stop')
async def stop(ctx):
    try:
        voice_clients[ctx.guild.id].stop()
        await voice_clients[ctx.guild.id].disconnect()
        del voice_clients[ctx.guild.id]
        await ctx.send("🛑 Stopped and disconnected.")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        print(e)
if not token:
    raise RuntimeError("DISCORD_TOKEN missing — check your .env and load_dotenv()")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
