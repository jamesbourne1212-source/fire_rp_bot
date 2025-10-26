import discord
from discord.ext import commands, tasks
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    if not check_timers.is_running():
        check_timers.start()

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

@tasks.loop(seconds=30)
async def check_timers():
    print("⏱ Checking timers... (every 30 seconds)")

@check_timers.before_loop
async def before_check_timers():
    await bot.wait_until_ready()

async def main():
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
