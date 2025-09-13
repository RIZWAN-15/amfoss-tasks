import discord
from discord.ext import commands
import asyncio

# ====== BOT SETUP ======
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # bot can read messages
2intents.members = True          # bot detects member joins

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== POWER 1: WELCOME & ROLE ASSIGNMENT ======
@bot.event
async def on_member_join(member):
    # find the #orientation channel
    channel = discord.utils.get(member.guild.text_channels, name="orientation")
    if channel:
        await channel.send(
            f"🎉 Welcome {member.mention} to Midtown Tech! You are now part of our friendly neighborhood. 🕷️"
        )

    # give default role "Aspiring Hero"
    role = discord.utils.get(member.guild.roles, name="Aspiring Hero")
    if role:
        await member.add_roles(role)

# ====== POWER 2: SPIDER-SENSE (MODERATION) ======
forbidden_keywords = [
    "villainous spam",
    "unauthorized link",
    "off-topic disruption",
    "menacing threats"
]

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # ignore bot’s own messages

    # check for forbidden content
    for keyword in forbidden_keywords:
        if keyword in message.content.lower():
            await message.delete()
            try:
                await message.author.send(
                    "⚠️ Your message was removed because it violated Midtown Tech's code of conduct. "
                    "Please keep the neighborhood friendly! 🕷️"
                )
            except:
                pass  # if DMs are closed
            return

    # allow other commands to still work
    await bot.process_commands(message)

# ====== POWER 3: DAILY BUGLE ANNOUNCEMENTS ======
@bot.command()
@commands.has_any_role("Faculty", "Administrator")  # only staff can use
async def bugle(ctx, *, message: str):
    # find #announcements channel
    channel = discord.utils.get(ctx.guild.text_channels, name="announcements")
    if not channel:
        await ctx.send("🚫 Announcements channel not found!")
        return

    msg = await channel.send(f"📰 **Daily Bugle Announcement** 📰\n{message}")

    # wait 24h (86400 seconds)
    await asyncio.sleep(86400)

    # delete only if not pinned
    if not msg.pinned:
        await msg.delete()

# ====== POWER 4: AUNT MAY'S WISDOM ======
wisdom_data = {
    "rules": "📜 Midtown Tech Rules:\n1. Be respectful.\n2. No spam.\n3. Stay on topic.",
    "resources": "📚 Helpful Resources:\n- https://docs.python.org\n- https://discordpy.readthedocs.io",
    "contact": "☎️ Contact Faculty:\nDM any Admin or Faculty role member."
}

@bot.command()
async def wisdom(ctx, topic: str):
    topic = topic.lower()
    if topic in wisdom_data:
        await ctx.send(wisdom_data[topic])
    else:
        await ctx.send("🤔 Unknown topic. Try: rules, resources, or contact.")

# Run bot
bot.run(TOKEN)
