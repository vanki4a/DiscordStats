import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import platform
import colorsys
import random
import os
import time
import io
import aiohttp
import urllib, json
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType
                
client=commands.Bot(command_prefix='/')
neshto='445198123837554688'


async def status_task():
    while True:
        await client.change_presence(game=discord.Game(name='/help | '+str(len(client.servers))+' servers',type=3))
        await asyncio.sleep(5)
	

	
@client.event
async def on_ready():
	print('Bot is online')
	print(client.user.name)
	print(client.user.id)      
	client.loop.create_task(status_task())

	
@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     

async def serverinfo(ctx):
    '''Displays Info About The Server!'''

    server = ctx.message.server
    roles = [x.name for x in server.role_hierarchy]
    role_length = len(roles)

    if role_length > 50: #Just in case there are too many roles...
        roles = roles[:50]
        roles.append('>>>> Displaying[50/%s] Roles'%len(roles))

    roles = ', '.join(roles);
    channelz = len(server.channels);
    time = str(server.created_at); time = time.split(' '); time= time[0];
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    join = discord.Embed(description= '%s '%(str(server)),title = 'Server Name', color = discord.Color((r << 16) + (g << 8) + b));
    join.set_thumbnail(url = server.icon_url);
    join.add_field(name = '__Owner__', value = str(server.owner) + '\n' + server.owner.id);
    join.add_field(name = '__ID__', value = str(server.id))
    join.add_field(name = '__Member Count__', value = str(server.member_count));
    join.add_field(name = '__Text/Voice Channels__', value = str(channelz));
    join.add_field(name = '__Roles (%s)__'%str(role_length), value = roles);
    join.set_footer(text ='Created: %s'%time);

    return await client.say(embed = join);
    
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def embed(ctx, *args):
    """
    Sending embeded messages with color (and maby later title, footer and fields)
    """
    argstr = " ".join(args)
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    text = argstr
    color = discord.Color((r << 16) + (g << 8) + b)
    await client.send_message(ctx.message.channel, embed=Embed(color = color, description=text))
    
@client.command(pass_context=True, aliases=['server'])
@commands.has_permissions(kick_members=True)
async def membercount(ctx, *args):
    """
    Shows stats and information about current guild.
    ATTENTION: Please only use this on your own guilds or with explicit
    permissions of the guilds administrators!
    """
    if ctx.message.channel.is_private:
        await client.delete_message(ctx.message)
        return

    g = ctx.message.server

    gid = g.id
    membs = str(len(g.members))
    membs_on = str(len([m for m in g.members if not m.status == Status.offline]))
    users = str(len([m for m in g.members if not m.bot]))
    users_on = str(len([m for m in g.members if not m.bot and not m.status == Status.offline]))
    bots = str(len([m for m in g.members if m.bot]))
    bots_on = str(len([m for m in g.members if m.bot and not m.status == Status.offline]))
    created = str(g.created_at)
    
    em = Embed(title="Membercount")
    em.description =    "```\n" \
                        "Members:   %s (%s)\n" \
                        "  Users:   %s (%s)\n" \
                        "  Bots:    %s (%s)\n" \
                        "Created:   %s\n" \
                        "```" % (membs, membs_on, users, users_on, bots, bots_on, created)

    await client.send_message(ctx.message.channel, embed=em)
    await client.delete_message(ctx.message)
    
@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)     
async def userinfo(ctx, user: discord.Member):
    """Informations for user."""
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="**__Name__**", value=user.name, inline=True)
    embed.add_field(name="**__ID__**", value=user.id, inline=True)
    embed.add_field(name="**__Status__**", value=user.status, inline=True)
    embed.add_field(name="**__Highest role__**", value=user.top_role)
    embed.add_field(name="**__Joined__**", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)

@client.command(pass_context = True)
@commands.has_permissions(manage_nicknames=True)     
async def setnick(ctx, user: discord.Member, *, nickname):
    await client.change_nickname(user, nickname)
    await client.delete_message(ctx.message)

@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)      
async def ban(ctx,user:discord.Member): 
    if user.server_permissions.ban_members:
        await client.say('**:x: I can`t ban this user.**')
        return

    try:
        await client.ban(user)
        await client.say(user.name+' **:white_check_mark: Successfully banned!**')
        await client.delete_message(ctx.message)
         
    except discord.Forbidden:

        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('ban failed.')
        return

@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def bans(ctx):
    '''Gets a list of users eho are no longer with us'''
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of the banned members", description = x, color = 0xFFFFF)
    return await client.say(embed = embed)

@client.command(pass_context=True)  
@commands.has_permissions(ban_members=True)     


async def unban(ctx):
   
    ban_list = await client.get_bans(ctx.message.server)

    # Show banned users
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    # Unban last banned user
    if not ban_list:
    	
        await client.say('Ban list is empty.')
        return
    try:
        await client.unban(ctx.message.server, ban_list[-1])
        await client.say('Unbanned user: `{}`'.format(ban_list[-1].name))
    except discord.Forbidden:
        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('unban failed.')
        return

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)

async def unbanall(ctx):
    server=ctx.message.server
    ban_list=await client.get_bans(server)
    await client.say('Unbanning {} members'.format(len(ban_list)))
    for member in ban_list:
        await client.unban(server,member)

@client.command(pass_context = True)

@commands.has_permissions(manage_roles=True)     
async def role(ctx, user: discord.Member, *, role: discord.Role = None):
        if role is None:
            return await client.say("You haven't specified a role! ")

        if role not in user.roles:
            await client.add_roles(user, role)
            return await client.say("{} ``role has been added to`` {}.".format(role, user))
            
        if role in user.roles:
            await client.remove_roles(user, role)
            return await client.say("{} ``role has been removed from`` {}.".format(role, user))
		
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def say(ctx, *, msg = None):
    await client.delete_message(ctx.message)

    if not msg: await client.say("Please specify a message to send")
    else: await client.say(msg)
    return
 
@client.command(pass_context = True)
@commands.has_permissions(manage_messages=True)  
async def clear(ctx, number):
 
    if ctx.message.author.server_permissions.manage_messages:
         mgs = [] #Empty list to put all the messages in the log
         number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number+1):
        mgs.append(x)            
       
    try:
        await client.delete_messages(mgs)          
        await client.say(str(number)+' messages deleted')
     
    except discord.Forbidden:
        await client.say(embed=Forbidden)
        return
    except discord.HTTPException:
        await client.say('clear failed.')
        return         
   
 
    await client.delete_messages(mgs)
	
@client.command(pass_context=True)
async def poll(ctx, question, *options: str):
        if len(options) <= 1:
            await client.say('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await client.say('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['👍', '👎']
        else:
            reactions = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001f51f']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(title=question, description=''.join(description), color = discord.Color((r << 16) + (g << 8) + b))
        react_message = await client.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await client.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await client.edit_message(react_message, embed=embed)
	
@client.command(pass_context=True)
async def guess(ctx, number):
    try:
        arg = random.randint(1, 10)
    except ValueError:
        await client.say("Invalid number")
    else:
        await client.say('The correct answer is ' + str(arg))

@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)     
async def kick(ctx,user:discord.Member):
    if user.server_permissions.kick_members:
        await client.say('**:x: I can`t kick that user.**')
        return
    
    try:
        await client.kick(user)
        await client.say(user.name+' :white_check_mark: **Successfully kicked!**')
        await client.delete_message(ctx.message)

    except discord.Forbidden:
        await client.say('Permission denied.')
        return	

	
@client.command(pass_context=True)  
@commands.has_permissions(kick_members=True)
async def getuser(ctx, role: discord.Role = None):
    if role is None:
        await client.say('**There is no "STAFF" role on this server!**')
        return
    empty = True
    for member in ctx.message.server.members:
        if role in member.roles:
            await client.say("{0.name}: {0.id}".format(member))
            empty = False
    if empty:
        await client.say("Nobody has the role {}".format(role.mention))

@client.command(pass_context = True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, userName: discord.User, *, message:str): 
    await client.send_message(userName, "You have been warned for ``<->`` **{}**".format(message))
    await client.say(":white_check_mark: {0} Has been warned! Reason ``<->`` **{1}** ".format(userName,message))
    pass

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True) 
async def roles(context):
	"""Displays all of the roles with their ids"""
	roles = context.message.server.roles
	result = "**__The roles are:__** "
	for role in roles:
		result += '``' + role.name + '``' + "<->" + '``' + role.id + '``' + "\n "
	await client.say(result)		
	
@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))

@client.command(pass_context=True, no_pm=True)
async def avatar(ctx, member: discord.Member):
    """User Avatar"""
    await client.reply("{}".format(member.avatar_url))		
	
@client.command(pass_context=True)
async def ping(ctx):
    t = await client.say('Pong!')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await client.edit_message(t, new_content=':timer: Pong! Client: {}ms'.format(int(ms)))

@client.command()
async def rps():
    await client.say(""":game_die: **RockPaperScissors** :game_die:""")                                 
    await client.say("Type /choose rock/paper/scissors to make your choice for the round.  First to 3 points wins!")
    global playingRPS
    playingRPS = True

@client.command()
async def choose(rockPaperOrScissors):
    global playingRPS, aiChoice, playerChoice, aiPoints, playerPoints

    if playingRPS is False:
        await client.say("Type /rps to play a game of rock paper scissors!")
        return

    #AI choice
    aiChoice = random.randrange(1,4)
    choiceList = {1:"rock", 2:"paper", 3:"scissors"}

    #Player choice
    if str.lower(rockPaperOrScissors) == "rock": playerChoice = 1
    if str.lower(rockPaperOrScissors) == "paper": playerChoice = 2
    if str.lower(rockPaperOrScissors) == "scissors": playerChoice = 3

    #See who won
    await client.say("You picked: " + rockPaperOrScissors + " and AI picked: " + choiceList[aiChoice] + ".")
    if playerChoice is 1 and aiChoice is 3 or playerChoice is 2 and aiChoice is 1 or playerChoice is 3 and aiChoice is 2:
        playerpoints += 1
        await client.say("You win the round!")
    elif playerChoice == aiChoice:
        await client.say("Tie!")
    else:
        aiPoints += 1
        await client.say("AI wins the round!")

    #End game if someone hit 3 points
    if playerPoints == 3:
        await client.say("You hit 3 points.  You win!")
        await endRPS()
        return
    if aiPoints == 3:
        await client.say("AI hit 3 points.  You lose!")
        await endRPS()
        return
    await client.say("Type /choose `<rock/paper/scissors>` to continue. ")
    await client.say("SCORE -> Player: " + str(playerPoints) + " AI: " + str(aiPoints))

@client.command(pass_context = True)
async def invite(ctx):
    author = ctx.message.author
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name = 'Join in support server! ',value =' **https://discord.gg/dp6Em5q** ',inline = False)
    embed.add_field(name = 'Invite! ',value =' **https://discordapp.com/api/oauth2/authorize?client_id=562959056357294100&permissions=8&scope=bot** ',inline = False)	
    await client.send_message(author,embed=embed)
    await client.say('📨 Check DMs! ')
     
client.run(os.getenv('Token'))
