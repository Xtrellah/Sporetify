import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="//", intents=intents)

# Join VC
async def join_voice(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        return await channel.connect()
    else:
        await ctx.send("Join a voice channel mf!")
        return None

# YT Search
def get_youtube_audio_url(query):
    ydl_opts = {
        "format": "bestaudio",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info["entries"][0]["url"]

# Play 
@bot.command()
async def play(ctx, *, query):
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not vc or not vc.is_connected():
        vc = await join_voice(ctx)
        if not vc:
            return

    url = get_youtube_audio_url(query)

    vc.stop()
    ffmpeg_opts = {"options": "-vn"}
    vc.play(discord.FFmpegPCMAudio(url, **ffmpeg_opts))

    await ctx.send(f"Here u go: **{query}**")

@bot.command()
async def stop(ctx):
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if vc and vc.is_connected():
        await vc.disconnect()
        await ctx.send("Alr fuck u too.")

bot.run("")
