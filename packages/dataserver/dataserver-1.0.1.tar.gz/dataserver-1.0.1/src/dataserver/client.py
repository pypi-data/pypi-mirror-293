"""For security reasons, the token is blank. If you want to host it yourself, follow:
1. Create a discord server.
2. Make 2 applications or use client.py but modify the token
3. Add those 2 applications to ur server with message intents and message permissions (If you don't plan to add people, use admin for convinence)
4. Reset 1 of the application's token and copy it. This will be the server's token.
5. Paste it in the token var
6. Reset the other application's token and copy it. This will by the clients' token.
7. Paste it in the "client.py"'s token var.
This is the storage solution for everyone, including beginners. It does not need money or skill. Just provide ur username and password, maybe data as a dict() and the storage works fine for some basic information. Altho it looks secure, it is not. So don't use it for private information."""
token = ""
import discord
import ast, json
__all__ = ["get, set"]
intents = discord.Intents.all()
intents.message_content = True
loginuser = ""

client = discord.Client(intents=intents)

# Function to send a message to a specific channel or default to "general"
async def send_message(content, channel_id=None):
    if channel_id is None:
        # Assuming the bot is in a single server, find the "general" channel
        for guild in client.guilds:
            channel = discord.utils.get(guild.text_channels, name="general")
            if channel:
                break
    else:
        channel = client.get_channel(channel_id)
    
    if channel:
        await channel.send(content)

# Event handler for when a message is received
    # Do something with the content here (e.g., process commands)
# Event handler for when the bot is ready
ready = 0
@client.event
async def on_ready():
    global ready
    ready = 1
    print("The module is ready.")
def check(message):
    return message.author != client.user
def is_ready():
    """Is the module ready? I don't know. Use it, it returns 1 (ready) and 0 (not ready) or just log the print statements idk"""
    return ready
# Function to handle login
async def get(user: str, password: str) -> dict:
    """Function for getting data. To create new user, just type the desired new username and password and it will return {}. Wrong passwords also return {}."""
    data = ""
    await send_message(f"login {user} {password}")
    m = (await client.wait_for("message", check=check)).content
    while not m == user + " end":
        if m.startswith(user + " content "):
            data += " ".join(m.split(" ")[2:])
        m = (await client.wait_for("message", check=check)).content
    return ast.literal_eval(data)
async def set(user: str, password: str, data: dict) -> None:
    content = json.dumps(data)
    content = [content[i:i + 1500] for i in range(0, len(content), 1500)]
    await send_message("sett " + user + " " + password)
    for i in content:
        await send_message("seta" + " " + i)
    await send_message(user + " end")
# Replace 'YOUR_BOT_TOKEN' with your bot's token
client.run(token)