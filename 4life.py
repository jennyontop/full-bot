from discord.enums import NotificationLevel
from discord.errors import HTTPException
from youtube_dl import YoutubeDL
from discord_components import DiscordComponents, Button, ButtonStyle
import discord
from discord.utils import get
import random
from discord.voice_client import VoiceClient
from discord.ext.commands import has_permissions, MissingPermissions, MissingRequiredArgument, BadArgument, BucketType, CommandOnCooldown, cooldown
from itertools import cycle
import os
import json
import asyncio
from discord.ext import commands
from random import choice
from discord import Embed
from discord_slash import SlashCommand, SlashContext
from io import BytesIO
import discord_pfp_banner_generator
import datetime
from datetime import timedelta
from PIL import Image
import requests

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix = "4", intents = intents)

mainshop = [{"name": "Watch", "price": 100, "description": "Time"},
            {"name": "Laptop", "price": 1000, "description": "Work"},
            {"name": "PC", "price": 10000, "description": "Gaming"}]

client.remove_command("help")
status = cycle(['.gg/jen for egirls', 'boost .gg/jen', f'{len(client.guilds)} guilds'])

client.lavanodes = [
    {
        'host': 'lava.link',
        'port': 80,
        'rest_url': f'http://lava.link:80',
        'identifier': 'MAIN',
        'region': 'singapore'
    }
]

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.dnd, activity = discord.Game(name = "giving seli head"))
    DiscordComponents(client)
    print(f'{client.user} is ready!')
    print('☆:.｡.o(≧▽≦)o.｡.:☆')

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:

        with open('reactembed.json') as react_file:

            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id = x['role_id'])

                    await payload.member.add_roles(role)


if os.path.exists(os.getcwd() + "./config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "4"}

    with open(os.getcwd() + "./config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

@client.command()
async def ping(ctx):
    await ctx.send(f'<:ThumbsUpSmile:853472258805465088> pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['it is certain.',
                'it is decidely so.',
                'without a doubt',
                'yes - definitely',
                'you may rely on it.',
                'as I see it, yes.',
                'most likely.',
                'outlook good.',
                'yes.',
                'yeah more than emma',
                'signs point to yes.',
                'reply hazy, try again.',
                'ask again later.',
                'better not tell you now',
                'cannot predict now.',
                'concentrate and ask again.',
                'dont count on it',
                'my reply is a No.',
                'my sources say no.',
                'outlook not so good.',
                'very doubtful.']
    await ctx.send(f'question: {question}\nanswer: {random.choice(responses)}')

@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.send(f'messages Purged by {ctx.message.author.mention}!')
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to clear messages!')

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'user {member} has been kicked!')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to kick someone!')

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'user {member} has been banned!')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to ban someone!')

@client.command()
@has_permissions(administrator = True)
async def massunban(ctx):
    banlist = await ctx.guild.bans()
    for users in banlist:
        try:
            await ctx.guild.unban(user=users.user)
        except:
            pass
        await ctx.send("mass unbanning...")

@massunban.error
async def massunban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to massunban banned members!')

@client.command()
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    mbed = discord.Embed(
        title = 'YAY!',
        description = f"{user} has successfully been unbanned.",
        color = color
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed=mbed)
        await guild.unban(user=user)

@client.command()
@has_permissions(manage_channels = True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + "is now locked.")

@lock.error
async def lock_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to lock a channel!')

@client.command()
@has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send( ctx.channel.mention + "is now unlocked.")

@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to unlock a channel!')

@client.command()
@has_permissions(manage_channels = True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"i've set the slowmode delay in this channel to {seconds} seconds.")

@slowmode.error
async def slowmode_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to apply slowmode in a channel!')

@client.command()
@has_permissions(manage_messages = True)
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL ", description=f"{message}", color = color)
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to create polls!')

@client.command(aliases=['av'])
async def avatar(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author

    memberAvatar = member.avatar_url

    avaEmbed = discord.Embed(title=f"{member.name}'s avatar", color = color)
    avaEmbed.set_image(url = memberAvatar)
    avaEmbed.set_footer(text = f"{member.name}'s avatar", icon_url = memberAvatar)

    await ctx.send(embed=avaEmbed)

@client.command(aliases=['cmd', 'commands', 'cmds'])
async def help(ctx):
    cmdEmbed = discord.Embed(title = '4life help menu', url = "https://poki-botmc.gitbook.io/autumn/", color = color)
    cmdEmbed.description = "my prefix : `4` | warning : commands are untogglable \n\n **`4{command}`** \n\n __anti-nuke__ \n __moderation__ \n __info__ \n __fun__ \n __action__ \n __economy__ \n __math__"
    cmdEmbed.set_image(url = "https://media.discordapp.net/attachments/903496560636203018/903553050868854804/image0.png?width=345&height=431")
    cmdEmbed.set_footer(text = f"© 17#7171", icon_url = f"{ctx.author.avatar_url}")

    await ctx.send(
        embed = cmdEmbed
    )

@client.command(aliases=['AntiNuke', 'anti-nuke', 'Antinuke', 'an', 'AN'])
async def antinuke(ctx):
    e = discord.Embed(title = "4life", description = "**antinuke** \n\n `massunban`, `unwhitelisted user banning - auto-on banned`, `antispam`", color = color)
    await ctx.send(embed = e)

@client.command(aliases=['mod', 'Mod'])
async def moderation(ctx):
    em = discord.Embed(description = "<:03heartw:900463610499837992> **moderation** \n\n `ban`, `kick`, `unban`, `lock`, `unlock`, `clear`, `slowmode`, `gcreate`, `mute`, `unmute`, `giverole`, `removerole`, `setnickname`, `warn`, `createrole`, `nuke <channel>`, `reactembed`, `createchannel`, `deleteemoji <emoji>`, `setwelcome/goodbyechannel`", color = color)
    await ctx.send(embed = em)

@client.command(aliases=['Info', 'info', 'Information'])
async def information(ctx):
    emb = discord.Embed(description = "<:03heartb:900463565033574440> **information** \n\n `avatar`, `help`, `whois`, `serverinfo`, `owner`, `membercount`, `invites`, `boosts`, `pngbanner`, `gifbanner`", color = color)
    await ctx.send(embed = emb)

@client.command(aliases=['Fun'])
async def fun(ctx):
    embed = discord.Embed(description = "<:bearhugs:903559509811814440> **fun** \n\n `8ball`, `ping`, `poll`, `meme`, `echo`, `rps`, `randomnumber`, `enlarge`, `snipe`, `spotify`", color = color)
    await ctx.send(embed = embed)

@client.command(aliases = ['Action'])
async def action(ctx):
    e = discord.Embed(description = "<:beartears:901156040828137493> **action** \n\n `smile`, `cry`, `hug`, `kiss`, `kill`, `slap`, `fuck`", color = color)
    await ctx.send(embed = e)

@client.command(aliases = ['Economy'])
async def economy(ctx):
    em = discord.Embed(description = "<:pocoyo1:903303720543092737> **economy** \n\n `bal`, `give`, `beg`, `withdraw`, `dep`, `shop`, `buy`", color = color)
    await ctx.send(embed = em)

@client.command()
async def math(ctx):
    emb = discord.Embed(description = "**Math** \n\n `add`, `subtract`, `divide`, `multiply` \n\n how to run : `4divide 8 2`", color = color)
    await ctx.send(embed = emb)

@client.command()
async def serverinfo(ctx):
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    serverinfoEmbed = discord.Embed(timestamp=ctx.message.created_at, color = color)
    serverinfoEmbed.set_thumbnail(url=ctx.guild.icon_url)
    serverinfoEmbed.add_field(name="server name", value=f"{ctx.guild.name}", inline=False)
    serverinfoEmbed.add_field(name="member count", value=ctx.guild.member_count, inline=False)
    serverinfoEmbed.add_field(name="verification level", value=str(ctx.guild.verification_level), inline=False)
    serverinfoEmbed.add_field(name="highest role", value=ctx.guild.roles[-2], inline=False)
    serverinfoEmbed.add_field(name="number of roles", value=str(role_count), inline=False)
    serverinfoEmbed.add_field(name="bots", value=', '.join(list_of_bots), inline=False)
    serverinfoEmbed.add_field(name="server name", value=f"{ctx.guild.name}", inline=False)

    await ctx.send(embed = serverinfoEmbed)

player1 = ""
player2 = ""
turn = ""
gameOver = True

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command(aliases=['ttt'])
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        nun = random.randint(1, 2)
        if nun == 1:
            turn = player1
            await ctx.send("it is <@" + str(player1.id) + ">'s turn.")
        elif nun == 2:
            turn = player2
            await ctx.send("it is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("a game is already in progress! finish it before starting a new one.")

@client.command()
async def place(ctx, pos : int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                if gameOver:
                    await ctx.send( mark + " wins!")
                elif count >= 9:
                    await ctx.send("it's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1

                
                
            else:
                await ctx.send("be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile")
        else:
            await ctx.send("it's not your turn.")
    else:
        await ctx.send("please start a new game!")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("please mention 2 players for this game.")
    elif isinstance(error, BadArgument):
        await ctx.send("please mention players (ie. <@771721105701601360>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("please enter a position you would like to mark.")
    elif isinstance(error, BadArgument):
        await ctx.send("please enter an integer.")   

@client.command()
@has_permissions(administrator = True)
async def gcreate(ctx, time=None, *, prize=None):
    if time == None:
        return await ctx.send("please include a time!")
    elif prize == None:
        return await ctx.send("please include a prize!")
    embed = discord.Embed(color = color, title = "new giveaway", description = f"{ctx.author.mention} is giving away **{prize}**!!")
    time_convert = {"s":1, "m":60, "h":3600, "d":86400}
    gawtime = int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text=f"giveaway ends in {time}")
    gaw_msg = await ctx.send(embed = embed)

    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)

    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)

    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"YAYYY!! {winner.mention} has won the giveaway for **{prize}**!!")

@gcreate.error
async def gcreate_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to create a giveaway!')

memes = [
    'https://static.thehoneycombers.com/wp-content/uploads/sites/4/2020/03/Best-funny-Coronavirus-memes-2020-Honeycombers-Bali-6.jpg',
    'https://i.pinimg.com/originals/ca/56/29/ca56291823db571427b44d18dee60ac8.jpg',
    'https://i.pinimg.com/originals/e3/2c/e7/e32ce76b21b7953e0badb1eceffff524.jpg',
    'https://video-images.vice.com/articles/5dfcdf5174a820009a1b4a41/lede/1576853802436-chicky-nuggies.jpeg?crop=1xw%3A1xh%3Bcenter%2Ccenter&resize=2000%3A*',
    'https://static.thehoneycombers.com/wp-content/uploads/sites/4/2020/03/Best-funny-Coronavirus-memes-2020-Honeycombers-Bali-10.jpg',
    'https://www.dictionary.com/e/wp-content/uploads/2018/03/bofa.jpg',
    'https://i.pinimg.com/550x/7d/e9/b6/7de9b6027ef8e14fb05fafe7ad18d076.jpg',
    'https://i.chzbgr.com/original/9607097856/h462A066B/funny-memes-deez-nuts-movie-characters'
]

@client.command()
async def meme(ctx):
    memeembed = discord.Embed(title = "meme", color = color)
    meme_random_link = random.choice(memes)
    memeembed.set_image(url = meme_random_link)
    await ctx.send(embed = memeembed)

smilegifs = [
    'https://c.tenor.com/3fAZZncIHDQAAAAC/smile-anime.gif',
    'https://i.pinimg.com/originals/3f/ed/52/3fed522a9f74fc39d4c265ab17a82267.gif',
    'https://c.tenor.com/n8oAtL1ti-QAAAAC/smile-anime.gif'
]

@client.command()
async def smile(ctx):
    smileembed = discord.Embed(description = f"{ctx.author.mention} smiled...", color = color)

    smile_random_link = random.choice(smilegifs)

    smileembed.set_image(url = smile_random_link)

    await ctx.send(embed = smileembed)

crygifs = [
    'https://media0.giphy.com/media/ROF8OQvDmxytW/giphy.gif',
    'https://64.media.tumblr.com/51f887bec04167f5588406913fc426a9/454b60c1ee3afe8d-79/s500x750/55d5b29f237a1456c5b9f54bddffdec47cb5b959.gifv',
    'https://data.whicdn.com/images/317306631/original.gif'
]

@client.command()
async def cry(ctx):
    cryembed = discord.Embed(description = f"{ctx.author.mention} cried...", color = color)

    cry_random_link = random.choice(crygifs)

    cryembed.set_image(url = cry_random_link)

    await ctx.send(embed = cryembed)

huggifs = [
    'https://i.pinimg.com/originals/8d/ab/29/8dab296aed2cbe25af8ebb4703517356.gif',
    'https://i.pinimg.com/originals/02/d9/ca/02d9cae34993e48ab5bb27763d5ca2fa.gif',
    'https://c.tenor.com/1T1B8HcWalQAAAAC/anime-hug.gif'
]

@client.command()
async def hug(ctx, *, member):
    hugembed = discord.Embed(description = f"aww! {ctx.author.mention} hugged {member}", color = color)

    hug_random_link = random.choice(huggifs)

    hugembed.set_image(url = hug_random_link)

    await ctx.send(embed = hugembed)

kissgifs = [
    'https://www.icegif.com/wp-content/uploads/anime-kiss-icegif-1.gif',
    'https://media3.giphy.com/media/G3va31oEEnIkM/giphy.gif',
    'https://www.icegif.com/wp-content/uploads/anime-kiss-icegif.gif'
]

@client.command()
async def kiss(ctx, *, member):
    kissembed = discord.Embed(description = f"cute! {ctx.author.mention} kissed {member}", color = color)

    kiss_random_link = random.choice(kissgifs)

    kissembed.set_image(url = kiss_random_link)

    await ctx.send(embed = kissembed)

killgifs = [
    'https://giffiles.alphacoders.com/696/69649.gif',
    'https://data.whicdn.com/images/159568456/original.gif',
    'https://i.pinimg.com/originals/42/dd/88/42dd884acd74ab8c3755e17cebc5c1d2.gif'
]

@client.command()
async def kill(ctx, *, member):
    killembed = discord.Embed(description = f"pew! {ctx.author.mention} killed {member}", color = color)

    kill_random_link = random.choice(killgifs)

    killembed.set_image(url = kill_random_link)

    await ctx.send(embed = killembed)

slapgifs = [
    'https://c.tenor.com/AzIExqZBjNoAAAAC/anime-slap.gif',
    'https://thumbs.gfycat.com/TerribleLightBagworm-max-1mb.gif',
    'https://i.imgur.com/fm49srQ.gif'
]

@client.command()
async def slap(ctx, *, member):
    slapembed = discord.Embed(description = f"LMAO! {ctx.author.mention} slapped {member}", color = color)

    slap_random_link = random.choice(slapgifs)

    slapembed.set_image(url = slap_random_link)

    await ctx.send(embed = slapembed)

fuckgifs = [
    'https://media.discordapp.net/attachments/840219136516423741/868344331499622420/20210724_120028.gif',
    'https://media.discordapp.net/attachments/840219136516423741/868344296435228702/20210724_120118.gif',
    'https://media.discordapp.net/attachments/840219136516423741/865479450082672640/20210716_142159.gif',
    'https://media.discordapp.net/attachments/884975254148112504/885533861012963338/image3.gif',
    'https://media.discordapp.net/attachments/884975254148112504/885303181985333258/image0.gif?width=418&height=427',
    'https://media.discordapp.net/attachments/884975254148112504/885303293939691520/image0.gif?width=487&height=427',
    'https://media.discordapp.net/attachments/884975254148112504/885302497034518538/image0.gif?width=478&height=427',
    'https://media.discordapp.net/attachments/884975254148112504/885302466479017984/image0.gif?width=514&height=427',
    'https://media.discordapp.net/attachments/840219136516423741/861427811650371584/20210705_100338.gif',
    'https://media.discordapp.net/attachments/840219136516423741/861427801198166026/20210705_100400.gif'
]

@client.command()
async def fuck(ctx, *, member):
    fuckembed = discord.Embed(description = f"ahh! {ctx.author.mention} fucked {member}", color = color)

    fuck_random_link = random.choice(fuckgifs)

    fuckembed.set_image(url = fuck_random_link)

    await ctx.send(embed = fuckembed)

@client.command()
@has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name = "Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name = "Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"muted {member.mention} for reason {reason}")
    await member.send(f"you were muted in the server : {guild.name} for the reason : {reason}")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to mute someone!')

@client.command()
@has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(ctx.guild.roles, name = "Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"unmuted {member.mention}")
    await member.send(f"you were unmuted in the server : {guild.name}")

@client.command()
async def echo(ctx, *, message=None):
    """
    A simple command that repeats the users input back to them.
    """
    message = message or "please provide a message to be repeated."
    await ctx.message.delete()
    await ctx.send(message)

@client.command(aliases=['own'])
async def owner(ctx):
    ownerembed = discord.Embed(color = color, title = "4life's owners :", description = "17#7171")

    await ctx.send(embed = ownerembed)

@client.command(aliases=['mc'])
async def membercount(ctx):
    guild = ctx.guild
    a = ctx.guild.member_count
    b = discord.Embed(title = f"members in {guild.name}", description = a, color = color)
    b.set_footer(text = f"Requested by {ctx.author.display_name}")
    await ctx.send(embed = b)

@client.command(pass_context=True)
@has_permissions(manage_roles = True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{ctx.author.mention}, {user.mention} has been given a role called: {role.name}")

@giverole.error
async def giverole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to give someone a role!')

@client.command(aliases=['setnick'], pass_context=True)
@has_permissions(administrator = True)
async def setnickname(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'nickname was changed for {member.mention} to {nick} ')

@setnickname.error
async def setnickname_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to change nicknames!')

@client.command()
@has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, arg):
    guild = ctx.guild.name
    user = member.mention
    warnembed = discord.Embed(title="Warning issued: ", color=color)
    warnembed.add_field(name="warning: ", value=f'reason: {arg}', inline=False)
    warnembed.add_field(name="user warned: ", value=f'{member.mention}', inline=False)
    warnembed.add_field(name="warned by: ", value=f'{ctx.author}', inline=False)

    await member.send(f'you have been warned in {guild} for **{arg}**!')
    message = await ctx.send(embed=warnembed)

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to warn someone!')

@client.command(help="Play with .rps [your choice]")
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    await ctx.send(f"rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in rpsGame

    user_choice = (await client.wait_for('message', check=check)).content

    comp_choice = random.choice(rpsGame)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(f'we tied! GG!\nyour choice: {user_choice}\nmy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'nice try, but I win this time!!\nyour choice: {user_choice}\nmy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"aw, you beat me. It won't happen again!\nyour choice: {user_choice}\nmy choice: {comp_choice}")

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(f'paper over rock duh.\nyour choice: {user_choice}\nmy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'oh, wacky. We just tied. I call a rematch!!\nyour choice: {user_choice}\nmy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"aw man, you actually managed to beat me.\nyour choice: {user_choice}\nmy choice: {comp_choice}")

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(f'LMFAO YOU LOST!\nyour choice: {user_choice}\nmy choice: {comp_choice}')
        elif comp_choice == 'paper':
            await ctx.send(f'bruh. >: |\nyour choice: {user_choice}\nmy choice: {comp_choice}')
        elif comp_choice == 'scissors':
            await ctx.send(f"oh well, we tied.\nyour choice: {user_choice}\nmy choice: {comp_choice}")

@client.command(aliases=['make_role'])
@has_permissions(manage_roles=True) # Check if the user executing the command can manage roles
async def createrole(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'role `{name}` has been created')

@createrole.error
async def createrole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to create roles!')

@client.command()
async def invites(ctx, usr: discord.Member=None):
    if usr == None:
       user = ctx.author
    else:
       user = usr
    total_invites = 0
    for i in await ctx.guild.invites():
        if i.inviter == user:
            total_invites += i.uses
    await ctx.send(f"{user.mention} has {total_invites} invite{'' if total_invites == 1 else 's'}!")

@client.command()
@has_permissions(administrator = True)
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("you did not mention a channel!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="has been Nuked!")
        await nuke_channel.delete()
        await new_channel.send("THIS CHANNEL HAS BEEN NUKED!")
        await ctx.send("nuked the Channel sucessfully!")

    else:
        await ctx.send(f"no channel named {channel.name} was found!")

@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to nuke channels!')

@client.command(aliases=['reactembed'])
@has_permissions(manage_messages = True)
async def reactionembed(ctx, emoji, role : discord.Role, *, message):

    reactembed = discord.Embed(color = color, description = message)
    msg = await ctx.channel.send(embed = reactembed)
    await msg.add_reaction(emoji)

    with open('reactembed.json') as json_file:
        data = json.load(json_file)

        new_react_role = {
            'role_name': role.name,
            'role_id': role.id,
            'emoji': emoji,
            'message_id': msg.id
        }

        data.append(new_react_role)

    with open('reactembed.json', 'w') as j:
        json.dump(data, j, indent = 4)

@reactionembed.error
async def reactionembed_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have admin permissions to make reaction embeds!')

@client.command(aliases = ['randomnum'])
async def randomnumber(ctx):

    # checks the author is responding in the same channel
    # and the message is able to be converted to a positive int
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("type a number")
    msg1 = await client.wait_for("message", check=check)
    await ctx.send("type a second, larger number")
    msg2 = await client.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"you got {value}.")
    else:
        await ctx.send("please ensure the first number is smaller than the second number.")

@client.command()
async def enlarge(ctx, emoji: discord.PartialEmoji or discord.Emoji = None):
    emojiurl = emoji.url
    enlargeembed = discord.Embed(description = "enlarged Emoji to :", color = color)
    enlargeembed.set_image(url = emojiurl)
    if not emoji:
        await ctx.send("you need to provide an emoji!")
    else:
        await ctx.send(embed = enlargeembed)

@client.command(aliases = ['serveravatar', 'serverav'])
async def servericon(ctx):
    serverAvatar = ctx.guild.icon_url

    servEmbed = discord.Embed(title=f"{ctx.guild.name}'s icon :", color = color)
    servEmbed.set_image(url = serverAvatar)
    servEmbed.set_footer(text = f"{ctx.guild.name}'s icon", icon_url = serverAvatar)

    await ctx.send(embed=servEmbed)

@client.command(pass_context=True)
@has_permissions(manage_roles = True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{ctx.author.mention}, {user.mention} has got a role removed: {role.name}")

@removerole.error
async def removerole_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to remove roles!')

@client.command(aliases = ['createchan'])
@has_permissions(manage_channels = True)
async def createchannel(msg):
    chan = await msg.guild.create_text_channel(name = "new channel")

    await msg.send(f"{chan.name} has been created.")

@createchannel.error
async def createchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('you dont have Admin Permissions to create channels!')

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await asyncio.sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@client.command()
async def snipe(ctx):
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = discord.Embed(color = color, title = f"last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f"Sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send(f"there are recently no deleted messages in {channel.mention}")

@client.command()
async def boosts(ctx):
    guild = ctx.guild.name
    boostcount = ctx.guild.premium_subscription_count
    boosticon = ctx.author.avatar_url

    boostembed = discord.Embed(color = color, title = "boost us!", description = f"boosts : {boostcount} , server : {guild}")
    boostembed.set_footer(text = f"by : {ctx.author.display_name}", icon_url = boosticon)

    await ctx.send(embed = boostembed)

@client.command(aliases=['whois'])
async def userinfo(ctx, *, member: discord.Member = None): # b'\xfc'
    if member is None:
        member = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=color, description=f"{member.mention}")
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="joined", value=member.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="registered", value=member.created_at.strftime(date_format))
    if len(member.roles) > 1:
        role_string = ' '.join([r.mention for r in member.roles][1:])
        embed.add_field(name="roles [{}]".format(len(member.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
    embed.add_field(name="guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='id: ' + str(member.id))
    return await ctx.send(embed=embed)

@client.command()
async def gifbanner(ctx, *, member : discord.Member = None):
    if member == None:
        member = ctx.author
    
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
    banner_id = req["banner"]
    # If statement because the member may not have a banner
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}.gif?size=1024"

    bannerembed = discord.Embed(
        description = f"{member.mention}'s banner :",
        color = color
    )
    bannerembed.set_image(url = banner_url)
    bannerembed.set_footer(text = f"Requested by {ctx.author}")

    await ctx.send(embed = bannerembed)

@client.command()
async def pngbanner(ctx, *, member : discord.Member = None):
    if member == None:
        member = ctx.author
    
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
    banner_id = req["banner"]
    # If statement because the member may not have a banner
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"

    bannerembed = discord.Embed(
        description = f"{member.mention}'s banner :",
        color = color
    )
    bannerembed.set_image(url = banner_url)
    bannerembed.set_footer(text = f"Requested by {ctx.author}")

    await ctx.send(embed = bannerembed)

@client.command()
@cooldown(5,10,BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(400)

    await ctx.send(f"congrats! someone gave you {earnings} coins!")

    users[str(user.id)]["wallet"] += earnings

    with open("bank.json", "w") as f:
        json.dump(users, f, indent=4)

@client.event
async def beg_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        msg = '__still on cooldown__ , please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0

async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has levelled up to **LEVEL {lvl_end}** !!')
        users[f'{user.id}']['level'] = lvl_end

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 250

    with open("bank.json", "w") as f:
        json.dump(users, f, indent=4)
    return True

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("bank.json", "w") as f:
        json.dump(users, f, indent=4)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["wallet"]]
    return bal

@client.command(aliases=['bal'])
async def balance(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    await open_account(member)

    users = await get_bank_data()
    user = member

    wallet_amount = users[str(user.id)]["wallet"]
    bank_amount = users[str(user.id)]["bank"]

    balembed = discord.Embed(title = f"{member.name}'s balance :", color = color)
    balembed.add_field(name = "wallet", value = wallet_amount)
    balembed.add_field(name = "bank", value = bank_amount)

    await ctx.send(embed = balembed)

@client.command()
async def give(ctx, member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("please enter an amount.")
        return 

    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal[0]

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("you don't have that much money!")
        return
    if amount<0:
        await ctx.send("amount must be positive!")
        return

    await update_bank(ctx.author, -1*amount, "bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"you gave {amount} coins!")

@client.command(pass_context=True)
async def slots(ctx, amount=None):

    if amount == None:
        await ctx.send("please enter an amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("you don't have that much money!")
        return
    if amount < 0:
        await ctx.send("amount must be positive")
        return

    slots = ['bus', 'train', 'horse', 'tiger', 'monkey', 'cow']
    slot1 = slots[random.randint(0, 5)]
    slot2 = slots[random.randint(0, 5)]
    slot3 = slots[random.randint(0, 5)]

    slotOutput = '| :{}: | :{}: | :{}: |\n'.format(slot1, slot2, slot3)

    ok = discord.Embed(title = "slots machine", color = color)
    ok.add_field(name = "{}\nWon".format(slotOutput), value = f'you won {2*amount} coins')


    won = discord.Embed(title = "Slots Machine", color = color)
    won.add_field(name = "{}\nWon".format(slotOutput), value = f'you won {3*amount} coins')
    

    lost = discord.Embed(title = "Slots Machine", color = color)
    lost.add_field(name = "{}\nLost".format(slotOutput), value = f'you lost {1*amount} coins')


    if slot1 == slot2 == slot3:
        await update_bank(ctx.author, 3 * amount)
        await ctx.send(embed = won)
        return

    if slot1 == slot2:
        await update_bank(ctx.author, 2 * amount)
        await ctx.send(embed = ok)
        return

    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.send(embed = lost)
        return

@client.command()
async def rob(ctx, member: discord.Member = None):
    if member == None:
        return await ctx.send("don't forget to mention who you'll rob LMAO!")
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)
    robberbal = await update_bank(ctx.author)
    if robberbal[0]<100:
        return await ctx.send("you need at least 100 coins to rob!")
    else:
        if bal[0]<100:
            return await ctx.send("the user does not have at least 100 coins...")

    stolen = random.randrange(-1*(robberbal[0]), bal[0])

    await update_bank(ctx.author, stolen)
    await update_bank(member, -1* stolen)

    if stolen > 0:
        return await ctx.send(f"you robbed {stolen} coins!")
    elif stolen < 0:
        stolen = stolen*-1
        return await ctx.send(f"you tried to steal but got caught LOL! You paid {stolen} coins!")

@client.command(aliases=['with'])
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("you don't have enough money")
        return

    if amount<0:
        await ctx.send("YOU CAN'T WITHDRAW A NEGATIVE AMOUNT")
        return

    await update_bank(ctx.author, amount, "wallet")
    await update_bank(ctx.author,-1*amount, "bank")

    await ctx.send(f"you withdrew {amount} coins!")

@client.command(aliases=['dep'])
async def deposit(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("please enter the amount")
        return

    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[1]
    elif amount == "max":
        amount = bal[1]

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("you don't have enough money")
        return

    if amount<0:
        await ctx.send("YOU CAN'T WITHDRAW A NEGATIVE AMOUNT")
        return

    await update_bank(ctx.author, -1*amount, "wallet")
    await update_bank(ctx.author, amount, "bank")

    await ctx.send(f"you deposited {amount} coins!")

@client.command()
async def shop(ctx):
    shopembed = discord.Embed(title = "shop", color = color)

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        shopembed.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = shopembed)

@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("that Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"you don't have enough money in your wallet to buy {amount} {item}")
            return

    await ctx.send(f"you just bought {amount} {item}")


async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = f"{user.name}'s inventory", color = color)
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)

@client.command(aliases = ['delemoji'])
async def deleteemoji(ctx, emoji: discord.Emoji):
    if ctx.author.guild_permissions.manage_emojis:
        await ctx.send(f"successfully deleted {emoji}")
        await emoji.delete()

color = 0x303135

@client.command()
async def botinfo(ctx):
    lol = discord.Embed(title = "my information :", url = "https://discord.com/api/oauth2/authorize?client_id=771721105701601360&permissions=8&scope=bot", color = color)
    lol.add_field(name = "id :", value = f"{client.user.id}", inline = True)
    lol.add_field(name = "created at :", value = "fri, Oct 30, 2020 9:04 AM", inline = True)
    lol.add_field(name = "owner", value = "17#7171", inline = True)
    lol.add_field(name = "main Command", value = f"{prefix}help", inline = True)
    lol.set_footer(text = "4LIFE LOL", icon_url = "https://images-ext-1.discordapp.net/external/-sofSYhlCHFe1wJv-L7hyeAx6Cv_GLFuxLuzdyC3VEU/%3Fsize%3D256/https/cdn.discordapp.com/avatars/771721105701601360/b0c9790e428dfbe4f1184563b019804e.png")

    await ctx.send(embed = lol)

@client.event
async def on_member_ban(guild, user):
      with open('whitelisted.json') as f:
        whitelisted = json.load(f)
      async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
      
        if str(guild.id) in whitelisted.keys():
            if str(i.user.id) in whitelisted[str(guild.id)]:
                return
    
        await guild.ban(i.user, reason="Anti-Nuke: Banning Members")
        await guild.kick(i.user, reason="Anti-Nuke: Banning Members")
        return

@client.event
async def on_member_join(member):
    welc = discord.Embed(title = f"welcome!", description = f"welcome! {member.mention}")
    name = member.name
    avatar = member.avatar_url
    welc.set_author(name = name, icon_url = avatar)
    welc.set_thumbnail(url = avatar)
    if clientdata.welcome_channel != None:
        await clientdata.welcome_channel.send(embed = welc)
        print(f"{member.name} joined a server.")

    else:
        print("welcome channel was not set.")

@client.event
async def on_member_remove(member):
    if clientdata.goodbye_channel != None:
        await clientdata.goodbye_channel.send(f"goodbye! {member.mention}")
        print(f"{member.name} left a server.")

    else:
        print("goodbye channel was not set.")
    
class ClientData:
    def __init__(self):
        self.welcome_channel = None
        self.goodbye_channel = None

clientdata = ClientData()

@client.command()
async def setwelcomechannel(ctx, channel_mention = None):
    if channel_mention != None:
        for channel in ctx.guild.channels:
            if channel.mention == channel_mention:
                clientdata.welcome_channel = channel
                welcome_channel = channel
                await ctx.channel.send(f"welcome channel has been set to : {channel.mention}")
                await channel.send("this is the new Welcome Channel!")

    else:
        await ctx.channel.send("you didn't state the welcome channel's name!")

@client.command()
async def setleavechannel(ctx, channel_mention = None):
    if channel_mention != None:
        for channel in ctx.guild.channels:
            if channel.mention == channel_mention:
                clientdata.goodbye_channel = channel
                goodbye_channel = channel
                await ctx.channel.send(f"leave channel has been set to : {channel.mention}")
                await channel.send("this is the new Leave Channel!")

    else:
        await ctx.channel.send("you didn't state the leave channel's name!")

@client.command()
@commands.guild_only() # We can only access activities from a guild
async def spotify(ctx, user: discord.Member = None):
    user = user or ctx.author  # default to the caller
    spot = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)
    if spot is None:
        await ctx.send(f"{user.name} is not listening to Spotify")
        return
    embedspotify = discord.Embed(title=f"{user.name}'s spotify song :", color=color)
    embedspotify.add_field(name="song", value=spot.title)
    embedspotify.add_field(name="artist", value=spot.artist)
    embedspotify.add_field(name="album", value=spot.album)
    embedspotify.set_thumbnail(url=spot.album_cover_url)
    await ctx.send(embed=embedspotify)

@client.command()
async def add(ctx, a: int, b: int):
    emb = discord.Embed(title = "answer :", description = a+b, color = color)
    emb.set_footer(text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = emb)

@client.command()
async def multiply(ctx, a: int, b: int):
    emb = discord.Embed(title = "answer :", description = a*b, color = color)
    emb.set_footer(text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = emb)

@client.command()
async def divide(ctx, a: int, b: int):
    divide25 = (a/b)
    emb = discord.Embed(title = "answer :", description = str(divide25), color = color)
    emb.set_footer(text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = emb)

@client.command()
async def subtract(ctx, num1 : float, num2 : float):
  answer = num1 - num2

  ans_em = discord.Embed(title = 'answer :', description = f'{answer}', color = color)
  ans_em.set_footer(text = f"Requested by {ctx.author.name}")

  await ctx.send(embed = ans_em)

async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

async def add_experience(users, user, exp, server):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(users, user, channel, server):
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1/4))
  
    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
        users[str(user.guild.id)][str(user.id)]['level'] = lvl_end


@client.command(aliases = ['rank','lvl'])
async def level(ctx,member: discord.Member = None):
    if not member:
        user = ctx.message.author
        with open('level.json','r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(user.id)]['level']
        exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP " ,color = discord.Color.green())
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
    else:
        with open('level.json','r') as f:
          users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(member.id)]['level']
        exp = users[str(ctx.guild.id)][str(member.id)]['experience']
        embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP" ,color = discord.Color.green())
        embed.set_author(name = member, icon_url = member.avatar_url)

        await ctx.send(embed = embed)

client.run(token)
