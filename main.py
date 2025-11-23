import discord
import os
import requests

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GROK_KEY = os.environ.get("GROK_KEY")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # mesaj içeriğini okuyabilmek için gerekli

bot = discord.Client(intents=intents)

# --- Grok API çağrısı ---
def ask_grok(message):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROK_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "grok-4.1-fast",
        "messages": [{"role": "user", "content": message}]
    }
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# --- Mesaj event ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # kendi mesajına cevap verme

    try:
        cevap = ask_grok(message.content)
        await message.channel.send(cevap)
    except Exception as e:
        await message.channel.send(f"❌ Hata: {e}")

# --- Botu çalıştır ---
bot.run(DISCORD_TOKEN)
