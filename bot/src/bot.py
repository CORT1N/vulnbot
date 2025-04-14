import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PUBLIC_CHANNEL_ID = os.getenv("PUBLIC_CHANNEL_ID")
HIDDEN_CHANNEL_ID = os.getenv("HIDDEN_CHANNEL_ID")

if not TOKEN:
    raise ValueError("Discord token not found.")
if not PUBLIC_CHANNEL_ID:
    raise ValueError("Discord public channel ID not found.")
if not HIDDEN_CHANNEL_ID:
    raise ValueError("Discord hidden channel ID not found.")


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    description="Use .vuln_help to get help.",
    )

@bot.event
async def on_ready() -> None:
    """Event triggered when the bot is ready."""
    print(f"Connected as {bot.user.name} - ID: {bot.user.id}")
    await bot.change_presence(activity=discord.Game(name="Use .vuln_help to get help."))

@bot.event
async def on_message(message) -> None:
    """Event triggered when a message is sent."""
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        await message.author.send(
            "I can't answer private messages.\n"
            "Please use the server to interact with me.",
            )
        return
    await bot.process_commands(message)

@bot.command(name="vuln_help")
async def vuln_help(ctx) -> None:
    """Command to display help."""
    if ctx.channel.id == PUBLIC_CHANNEL_ID:
        await ctx.author.send(
            "[DEBUG]: This bot is currently in debug mode, "
            "some permissions are too permissive.\n"
            "You can use `.unlock` in the command channel to "
            "get access to hidden channels.",
            )
    elif ctx.channel.id == HIDDEN_CHANNEL_ID:
        await ctx.author.send(
            """
            [DEBUG]: You are in the debug channel!
            Here are the new commands you can use:
            - `.ls [option(s)]`: List files in the current directory.
            - `.cat <file>` : Displays the content of the specified file.
            - `.net` : Displays the server's IP address.
            """,
        )
    else:
        await ctx.author.send(
            "You can only use this command in the bot-command channel !",
            )
    await ctx.message.delete()

@bot.command()
async def unlock(ctx) -> None:
    """Commande to unlock the hidden channel."""
    if ctx.channel.id == PUBLIC_CHANNEL_ID:
        hidden_channel = bot.get_channel(HIDDEN_CHANNEL_ID)
        if hidden_channel:
            await ctx.author.send(
                f"[DEBUG] Access granted! You can now see: {hidden_channel.mention} "
                "and use the commands `.ls`, `.cat` and `.net`.\n"
                "Warning, this permission should not have been granted...",
                )
            await hidden_channel.set_permissions(ctx.author, read_messages=True)
        else:
            await ctx.author.send("Problem with the hidden channel.")
    else:
        await ctx.author.send(
            "You can only use this command in the bot-command channel !",
        )

    await ctx.message.delete()

@bot.command()
async def ls(ctx, *args) -> None:
    """Commande to list files in the current directory."""
    if ctx.channel.id == HIDDEN_CHANNEL_ID:
        if args:
            files = []
            for path in args:
                if Path(path).exists():
                    if Path(path).is_dir():
                        files.extend(os.listdir(path))
                    else:
                        files.append(path)
                else:
                    files.append(f"[DEBUG] Specified path does not exists: {path}")
            await ctx.author.send(
                "\n".join(files) if files else "[DEBUG] No visible file...",
                )
        else:
            files = [f for f in os.listdir(".") if not f.startswith(".")]
            await ctx.author.send(
                "\n".join(files) if files else "[DEBUG] No visible file...",
                )
    else:
        await ctx.author.send("You do not have access to this command here.")

    await ctx.message.delete()

@bot.command()
async def cat(ctx, filename: str) -> None:
    """Command to display the content of a file."""
    if ctx.channel.id == HIDDEN_CHANNEL_ID:
        if Path(filename).exists():
            with open(filename) as f:
                content = f.read()

            max_length = 2000
            intro = f"[DEBUG] Reading file: {filename}\n"
            clean_content = content

            max_content_length = max_length - len(intro) - 7

            for i in range(0, len(clean_content), max_content_length):
                chunk = clean_content[i:i + max_content_length]
                if i == 0:
                    await ctx.author.send(f"```{intro}{chunk}```")
                else:
                    await ctx.author.send(f"```{chunk}```")
        else:
            await ctx.author.send(
                f"[DEBUG] File {filename} does not exist or is not accessible.",
                )
    else:
        await ctx.author.send("You do not have access to this command here.")

    await ctx.message.delete()

@bot.command()
async def net(ctx) -> None:
    """Command to display the server's IP address."""
    if ctx.channel.id == HIDDEN_CHANNEL_ID:
        await ctx.author.send(f"[DEBUG] Server IP Address: {os.getenv('SERVER_IP')}")
    else:
        await ctx.author.send("You do not have access to this command here.")

    await ctx.message.delete()

bot.run(TOKEN)
