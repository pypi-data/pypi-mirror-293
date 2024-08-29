"""For security reasons, the token is blank. If you want to host it yourself, follow:
1. Create a discord server.
2. Make 2 applications or use client.py but modify the token
3. Add those 2 applications to ur server with message intents and message permissions (If you don't plan to add people, use admin for convinence)
4. Reset 1 of the application's token and copy it. This will be the server's token.
5. Paste it in the token var
6. Reset the other application's token and copy it. This will by the clients' token.
7. Paste it in the "client.py"'s token var."""
token = ""
import discord
import json
def get_json(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {path} is not a valid JSON file.")
        return None
intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
async def send_message(content, channel_id=None):
    # If channel_id is not provided, default to "general" channel
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
def check(message):
    return message.author != client.user
@client.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == client.user:
        return
    
    # Example: Respond to a specific command
    content = message.content
    print(content)
    if content.startswith("login "):
        user = content.split(" ")[1]
        password = " ".join(content.split(" ")[2:])
        passwd = get_json("users.json")
        if user not in passwd:
            await send_message(user + " content {}")
            passwd[user] = password
            json.dump(passwd, open("users.json", "w"))
            a = get_json("data.json")
            a[user] = {}
            json.dump(a, open("data.json", "w"))
        elif passwd[user] == password:
            content = str(get_json("data.json")[user])
            content = [content[i:i + 1500] for i in range(0, len(content), 1500)]
            for i in content:
                await send_message(user + " content " + i)
        elif passwd[user] != password:
            await send_message(user + " content {}")
        await send_message(user + " end")
    elif content.startswith("sett "):
        user = content.split(" ")[1]
        password = " ".join(content.split(" ")[2:])
        passwd = get_json("users.json")
        data = ""
        if passwd[user] == password:
            m = (await client.wait_for("message", check=check)).content
            while m != user + " end":
                if m.startswith("seta "):
                    data += " ".join(m.split(" ")[1:])
                m = (await client.wait_for("message", check=check)).content
            a = get_json("data.json")
            a[user] = eval(data)
            json.dump(a, open("data.json", "w"))
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Replace 'YOUR_BOT_TOKEN' with your bot's token
client.run(token)
