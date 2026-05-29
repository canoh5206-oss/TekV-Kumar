import discord
from discord.ext import commands
import json
import os
import random

# Botun çalışması için gerekli izinler
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Coin/Ekonomi verilerini kaydedecek dosya
DATA_FILE = "ekonomi.json"

def veri_yukle():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def veri_kaydet(veri):
    with open(DATA_FILE, "w") as f:
        json.dump(veri, f, indent=4)

@bot.event
async def on_ready():
    print(f"{bot.user.name} başarıyla aktif oldu!")

# Örnek Kumar/Zar Komutu
@bot.command()
async def zar(ctx, miktar: int):
    veriler = veri_yukle()
    user_id = str(ctx.author.id)
    
    if user_id not in veriler:
        veriler[user_id] = 1000
        
    if veriler[user_id] < miktar:
        await ctx.send("Yeterli coinin yok!")
        return

    bot_zar = random.randint(1, 6)
    oyuncu_zar = random.randint(1, 6)
    
    if oyuncu_zar > bot_zar:
        veriler[user_id] += miktar
        await ctx.send(f"Kazandın! Zarlar: Sen [{oyuncu_zar}] - Bot [{bot_zar}]. Yeni Bakiyen: {veriler[user_id]}")
    elif oyuncu_zar < bot_zar:
        veriler[user_id] -= miktar
        await ctx.send(f"Kaybettin! Zarlar: Sen [{oyuncu_zar}] - Bot [{bot_zar}]. Kalan Bakiyen: {veriler[user_id]}")
    else:
        await ctx.send(f"Berabere! Zarlar: Sen [{oyuncu_zar}] - Bot [{bot_zar}]. Bakiyen değişmedi.")
        
    veri_kaydet(veriler)

# Kendi gizli bot tokenını alttaki tırnak işaretlerinin (" ") arasına yapıştır:
TOKEN = "MTUwOTg0ODMyMDU1NjkyNDk0OA.GUG8Oz.9L-wueUIHCqOHwSaD4TxUt7eAK-2KJwXSrGQzc"
bot.run(TOKEN)
