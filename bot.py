import discord
from discord import app_commands
from discord.ext import tasks
from typing import List
import api
import db
import time
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MY_GUILD = discord.Object(id=os.getenv('GUILD_ID'))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = MyClient(intents=discord.Intents.default())
 
@tasks.loop(seconds = 60)
async def watcher():
        players = db.get_watched_players()
        for player in players:
            await newMatchCheck(player[0],player[1])
            time.sleep(5) 

@client.event
async def on_ready():
    print(f'Starting bot as {client.user} ')
    print('------')
    watcher.start()


##===[WATCH ADD]===##
@client.tree.command()
@app_commands.describe(
    player='Display Name and tag of the player (name#tag)',
)
async def watchadd(ctx, player: str):
    """Add a player to watchlist in this channel."""
    await ctx.response.defer()
    try:
        name,tag = player.split('#')
    except:
        await asyncio.sleep(delay=0)
        return await ctx.followup.send(f':exclamation: Please send player in this format: name#tag')
        
    region = api.player_exists(name,tag)
    
    if not region:
        await asyncio.sleep(delay=0)
        return await ctx.followup.send(f':exclamation: `{player}` - Player Not Found!')
    
    if db.is_user_already_watched(player,str(ctx.channel.id)):
        await asyncio.sleep(delay=0)
        return await ctx.followup.send(f':exclamation: `{player}` - Player is already being watched!')
    
    last_match_id = api.player_last_match(player,region)['meta']['id']
    db.add_to_watchlist(player,str(ctx.channel.id),region,last_match_id)
    await asyncio.sleep(delay=0)
    return await ctx.followup.send(f':white_check_mark: Added `{player}` to watchlist in {ctx.channel.mention}.')


##===[WATCH REMOVE]===##
async def watchremove_autocomplete(
    ctx: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    w=db.get_watchlist(str(ctx.channel.id))   
    players = [item[0] for item in w]
    return [
        app_commands.Choice(name=player, value=player)
        for player in players if current.lower() in player.lower()
    ]
    
@client.tree.command()
@app_commands.describe(
    player='Display Name and tag of the player (name#tag)',
)
@app_commands.autocomplete(player=watchremove_autocomplete)
async def watchremove(ctx, player: str):
    """Remove a player from watchlist in this channel."""
    await ctx.response.defer()
    try:
        name,tag = player.split('#')
    except:
        await asyncio.sleep(delay=0)
        return await ctx.followup.send(f':exclamation: Please send player in this format: name#tag')
        
        
    if db.is_user_already_watched(player,str(ctx.channel.id)):
        db.remove_from_watchlist(player,str(ctx.channel.id))
        await asyncio.sleep(delay=0)
        return await ctx.followup.send(f':white_check_mark: `{player}` - Player has been removed from watchlist in {ctx.channel.mention}.')
    else:
        await asyncio.sleep(delay=0)
        return await ctx.followup.send(f':exclamation: `{player}` is not being watched in {ctx.channel.mention}.')


##===[WATCH LIST]===##
@client.tree.command()
async def watchlist(ctx):
    """List of players being watched in this channel."""
    await ctx.response.defer()
    watchlist = db.get_watchlist(str(ctx.channel.id))    
    if watchlist == None:
        await asyncio.sleep(delay=0)
        return await ctx.followup.send(f':white_square_button: **No player is being watched in {ctx.channel.mention}:**\n\n')
    await asyncio.sleep(delay=0)
    return await ctx.followup.send(f':white_square_button: **Watchlist for {ctx.channel.mention}:**\n\n'+'\n'.join(f"{i+1}. {item[0]}" for i, item in enumerate(watchlist)))

##===[WATCHER FUNCITONS]===##
async def newMatchCheck(player,region):
    last_match = api.player_last_match(player,region)
    cache_last_match_id = db.get_last_matchid(player)
    if last_match['meta']['id'] != cache_last_match_id:
        db.update_last_match(player,last_match['meta']['id'])
        await notifyNewMatch(player,last_match)
        return last_match
    return False

async def notifyNewMatch(player,match):
    mode = match['meta']['mode']
    mmap = match['meta']['map']['name']
    agentid = match['stats']['character']['id']
    team = match['stats']['team']
    ally_score = match['teams']['red'] if team == 'Red' else match['teams']['blue']
    opp_score  = match['teams']['red'] if team == 'Blue' else match['teams']['blue']
    score = match['stats']['score']
    kills = match['stats']['kills']
    deaths = match['stats']['deaths']
    assists = match['stats']['assists']
    has_won = ally_score > opp_score
    
    channels = db.get_player_channels(player)
    embed = discord.Embed(title=f"{player} won a {mode} game",
                      description=f"**{mode} - {ally_score}:{opp_score} - {mmap}**\n{score} Score - {kills}/{deaths}/{assists} KDA",
                      color=0x32DC65 if has_won else 0xFA4453)

    embed.set_thumbnail(url=f"https://media.valorant-api.com/agents/{agentid}/displayicon.png")
    embed.set_footer(text="Developed by @iamNVN")
    
    for id in channels:
        channel = client.get_channel(int(id))
        await channel.send(embed=embed)
 


client.run(TOKEN)
