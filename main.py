import random
import os
from datetime import date
import get_covid
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import asyncio
from mutagen.mp3 import MP3
from pydub import AudioSegment

client = commands.Bot(command_prefix='&')
client.remove_command('help')

komendy = ['help', 'ping', '8ball', '&clear', '&spam', '&covid', '&play', '&earrape', '&leave', '&kick']

# embed for command help
embed = discord.Embed(title="Dostępne komendy", color=0x0000ff)
embed.add_field(name="&ping", value="Zwracam twój aktualny ping", inline=False)
embed.add_field(name="&8ball", value="Odpowiadam na twoje pytanie", inline=False)
embed.add_field(name="&clear", value="Czyszczę podaną przez ciebie ilość wiadomości z czatu", inline=False)
embed.add_field(name="&spam", value="Co sekunde będe wysyłał podany przez ciebie wyraz", inline=False)
embed.add_field(name="&covid", value="Wysyłam ci post o dzisiejszej sytuacji w Polsce", inline=False)
embed.add_field(name="&play", value="Puszczam twój kawałek z linka", inline=False)
embed.add_field(name="&earrape", value="Prawie jak &play, ale może zauważysz różnicę", inline=False)
embed.add_field(name="&leave", value="Opuszczam kanał", inline=False)
embed.add_field(name="&kick", value="Wyrzucam wybranego przez ciebie użytkownika z kanału", inline=False)


# Bot is running properly
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Hello there"))
    print("Bot gotowy")


# Wrong command
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=embed)
        await ctx.message.delete()
    else:
        print(str(error))


# help command
@client.command()
async def help(ctx):
    await ctx.send(embed=embed)
    await ctx.message.delete()


# Return your ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Responds with random answer for your question
@client.command(aliases=['8ball'])
async def _8ball(ctx):
    responses = ['Jeszcze jak',
                 'Jak zawsze',
                 'Oczywiście',
                 'Nie no nie',
                 'Oczywiście że nie',
                 'Hm sam nie wiem, kolegi spytam',
                 'Nie odpowiem ci',
                 'Głupie pytanie']

    await ctx.send(f'{random.choice(responses)}')


# Clearing messages from chat
@client.command()
async def clear(ctx, amount=0):
    if amount == 0:
        await ctx.send(f'Nie powiedziałeś ile wiadomości mam usunąć!')
        return
    await ctx.channel.purge(limit=amount + 1)


# Bot is sending message every second
@client.command()
async def spam(ctx, text='Spam', amount=5):
    for i in range(0, amount):
        await ctx.send(text)
        await asyncio.sleep(1)


# Bot is sending embed with covid stats from Poland
@client.command(name="covid")
async def covid(ctx):
    result = get_covid.get_covid()
    day = date.today().strftime("%d/%m/%Y")

    embedc = discord.Embed(title="Status na dzień " + day, color=0xff0000)
    embedc.set_author(name="Pandemia Koronawirusa")
    embedc.add_field(name="Wykonane Testy", value=result[0], inline=False)
    embedc.add_field(name="Potwierdzone przypadki", value=result[1], inline=False)
    embedc.add_field(name="Wyzdrowiało", value=result[2], inline=False)
    embedc.add_field(name="Ofiary śmiertelne", value=result[3], inline=False)

    await ctx.send(embed=embedc)
    await ctx.message.delete()


# play //////////////////////////////////////////////////////////////////////////////////////////// playing song from yt
@client.command(pass_context=True)
async def play(ctx, url: str):
    global voice, name

    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Stary plik dzwiekowy usuniety")
    except PermissionError:
        print("Spróbowałem usunąć plik ale jest aktualnie używany")
        return

    await ctx.send("Już puszczam")

    ydl_opts = {
        'format': "bestaudio/best",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Pobieram audio\n")
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f"Zmieniona nazwa pliku: {file}\n")
            os.rename(file, "song.mp3")

    audio = MP3("song.mp3")
    print(audio.info.length)

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} Przestał grać"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing {nname[:2]}")
    print("Gram\n")
    await asyncio.sleep(audio.info.length)
    await voice.disconnect()


# earrape ////////////////////////////////////////////////////////////////////// playing song from yt with more decibels
@client.command(pass_context=True)
async def earrape(ctx, url):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    await ctx.message.delete()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Stary plik dzwiekowy usuniety")
    except PermissionError:
        print("Spróbowałem usunąć plik ale jest aktualnie używany")
        return

    await ctx.send("Sam tego chciałeś")

    ydl_opts = {
        'format': "bestaudio/best",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Pobieram audio\n")
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f"Zmieniona nazwa pliku: {file}\n")
            os.rename(file, "song.mp3")

    audio = MP3("song.mp3")
    song = AudioSegment.from_mp3("song.mp3")
    song = song + 50
    song.export("song.mp3", format='mp3')
    print(audio.info.length)

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} Przestał grać"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 10.00

    print("Gram\n")

    await asyncio.sleep(audio.info.length)
    await voice.disconnect()


# Leaving voice channel
@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Opuściłem {channel}")
    else:
        await ctx.send(f"Gościu jak mam wyjść jak nie ma mnie na kanale???")


# Kicking somebody from voice channel
@client.command()
async def kick(ctx, member: discord.Member):
    await member.edit(voice_channel=None)


client.run('TOKEN')
