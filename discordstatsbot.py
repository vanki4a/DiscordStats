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
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType

client=commands.Bot(command_prefix='ds!')
neshto='445198123837554688'

@client.event
async def on_ready():
	print('Bot is online')
	print(client.user.name)
	print(client.user.id)
	await client.change_presence(game=discord.Game(name='ds!help',type=3))

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
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="``ID``", value=user.id, inline=True)
    embed.add_field(name="``Status``", value=user.status, inline=True)
    embed.add_field(name="``Highest role``", value=user.top_role)
    embed.add_field(name="``Joined``", value=user.joined_at)
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
        await client.say(user.name+'was banned!')

    except discord.Forbidden:

        await client.say('Permission denied.')
        return
    except discord.HTTPException:
        await client.say('ban failed.')
        return

@client.command(pass_context = True)
@commands.has_permissions(administrator=True) 
async def bans(ctx):
    '''Gets A List Of Users Who Are No Longer With us'''
    x = await client.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "List of The Banned Idiots", description = x, color = 0xFFFFF)
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

	
@client.event
async def on_member_join(member):
    print("In our server" + member.name + " just joined")
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name='Welcome message')
    embed.add_field(name = '__Welcome to Our Server__',value ='**Hope you will be active here. Check Our server rules and never try to break any rules. ',inline = False)
    embed.set_image(url = 'https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif')
    await client.send_message(member,embed=embed)
    print("Sent message to " + member.name)
    channel = discord.utils.get(client.get_all_channels(), server__name='DarkBot Official Server', name='darkbot-servers-join-leave-log')
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title=f'Welcome {member.name} to {member.server.name}', description='Do not forget to check <#474572305192845312> and never try to break any one of them', color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name='__Thanks for joining__', value='**Hope you will be active here.**', inline=True)
    embed.add_field(name='Your join position is', value=member.joined_at)
    embed.set_image(url = 'https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif')
    embed.set_thumbnail(url=member.avatar_url)
    await client.send_message(channel, embed=embed)
	
@client.command()
async def invite():
	await client.say(':gift:')
	await client.say('https://discordapp.com/api/oauth2/authorize?client_id=562959056357294100&permissions=8&scope=bot')
  
client.run(os.getenv('Token'))
