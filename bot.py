import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

# ------------- CONFIG -------------
TOKEN = "MTQxMDgxODI0MDk1ODk1OTY0Mg.GZE5ul.m-dCWUweX4qg0KcWvNBAn64_fYCeLIJHabbLko"
UPDATE_INTERVAL = 60  # seconds between status updates
# ---------------------------------

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables to store server info
server_ip = "nicktop.win"
server_port = 25565


@tasks.loop(seconds=UPDATE_INTERVAL)
async def update_status():
    global server_ip, server_port
    if server_ip is None:
        return
    try:
        server = JavaServer.lookup(f"{server_ip}:{server_port}")
        status = server.status()
        player_count = status.players.online
        await bot.change_presence(
            activity=discord.Game(
                name=f"{player_count} players on {server_ip}")
        )
        print(f"Updated status: {player_count} players online")
    except Exception as e:
        print(f"Error pinging server: {e}")
        await bot.change_presence(activity=discord.Game(name="Server offline"))


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    update_status.start()

# -------- Commands --------


@bot.command()
async def setserver(ctx, ip: str, port: int = 25565):
    """Set the Minecraft server IP and optional port"""
    global server_ip, server_port
    server_ip = ip
    server_port = port
    await ctx.send(f"Server set to `{server_ip}:{server_port}`")


@bot.command()
async def status(ctx):
    """Check the current server status manually"""
    global server_ip, server_port
    if server_ip is None:
        await ctx.send("No server set yet. Use `!setserver <ip> [port]`.")
        return
    try:
        server = JavaServer.lookup(f"{server_ip}:{server_port}")
        status = server.status()
        await ctx.send(f"✅ {server_ip}:{server_port} is online with {status.players.online} players.")
    except Exception as e:
        await ctx.send(f"❌ Could not reach {server_ip}:{server_port} ({e})")

# ---------------------------

bot.run(TOKEN)
