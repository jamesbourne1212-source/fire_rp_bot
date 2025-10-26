import os
import asyncio
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ba_timers = {}

# --- Helper function ---
def format_time_left(minutes_left):
    if minutes_left <= 0:
        return "⏰ Time expired!"
    else:
        return f"{minutes_left} min left under air."

# --- Slash commands ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    if not check_timers.is_running():
        check_timers.start()
    try:
        await bot.tree.sync()
        print("✅ Slash commands synced")
    except Exception as e:
        print(f"❌ Sync error: {e}")

@bot.tree.command(name="engage_pump", description="Engage the fire pump.")
async def engage_pump(interaction: discord.Interaction):
    await interaction.response.send_message("🚒 Pump engaged. Pressure steady at 10 bar, guv’nor!")

@bot.tree.command(name="spray_hose", description="Spray the hose.")
async def spray_hose(interaction: discord.Interaction):
    await interaction.response.send_message("💦 Hose spraying — steady jet, good pressure!")

@bot.tree.command(name="cuts_windshield", description="Cut through the car windshield.")
async def cuts_windshield(interaction: discord.Interaction):
    await interaction.response.send_message("✂️ Crew cutting through the vehicle’s windscreen cleanly!")

@bot.tree.command(name="disconnect_battery", description="Disconnect the vehicle battery.")
async def disconnect_battery(interaction: discord.Interaction):
    await interaction.response.send_message("🔋 Vehicle battery disconnected, scene made safe!")

@bot.tree.command(name="visor_down", description="Lower your helmet visor.")
async def visor_down(interaction: discord.Interaction):
    await interaction.response.send_message("🪖 Visor down. Ready for entry, stay sharp!")

@bot.tree.command(name="under_air", description="Start BA timer for a firefighter.")
async def under_air(interaction: discord.Interaction, name: str, duration: int):
    end_time = datetime.now() + timedelta(minutes=duration)
    ba_timers[name] = end_time
    await interaction.response.send_message(f"⏱️ {name} is now under air for {duration} minutes.")

@bot.tree.command(name="status", description="Check BA status.")
async def status(interaction: discord.Interaction):
    if not ba_timers:
        await interaction.response.send_message("📋 No one is currently under air.")
        return

    msg = "🧯 **Current BA wearers:**\n"
    for name, end_time in ba_timers.items():
        remaining = (end_time - datetime.now()).total_seconds() / 60
        msg += f"• {name}: {format_time_left(int(remaining))}\n"
    await interaction.response.send_message(msg)

@bot.tree.command(name="end", description="End a BA session.")
async def end(interaction: discord.Interaction, name: str):
    if name in ba_timers:
        del ba_timers[name]
        await interaction.response.send_message(f"✅ {name}'s BA session ended.")
    else:
        await interaction.response.send_message("❌ That firefighter isn't currently under air.")

# --- BA timer background task ---
@tasks.loop(minutes=1)
async def check_timers():
    now = datetime.now()
    expired = [name for name, end_time in ba_timers.items() if now >= end_time]

    for name in expired:
        del ba_timers[name]
        channel = discord.utils.get(bot.get_all_channels(), name="entry-control")
        if channel:
            await channel.send(f"🚨 **ALARM:** {name}'s air time has expired! Evacuate immediately!")
        else:
            print(f"⚠️ No #entry-control channel found for expired timer: {name}")

# --- Entrypoint for Render ---
async def main():
    token = os.getenv("TOKEN")
    if not token:
        print("❌ Missing TOKEN environment variable")
        return
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually")
