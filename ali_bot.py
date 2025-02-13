import discord
import requests
import os

# Load environment variables (Replace with actual keys or set as environment variables)
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_DISCORD_BOT_TOKEN")  # Replace with your bot token
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "YOUR_DEEPSEEK_API_KEY")  # Replace with DeepSeek API key

# Initialize Discord bot
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Function to get AI response from DeepSeek API
def get_deepseek_response(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "Error: Unable to get response from DeepSeek."

# Bot Event Listeners
@client.event
async def on_ready():
    print(f'🚀 ALi is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ali"):
        prompt = message.content[5:].strip()  # Remove "!ali" prefix
        if not prompt:
            await message.channel.send("**Usage:** !ali <message>")
            return
        
        response = get_deepseek_response(prompt)
        await message.channel.send(f"**ALi:** {response}")

# Run the bot
client.run(TOKEN)
