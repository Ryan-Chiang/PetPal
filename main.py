import datetime
import json
import logging
import asyncio, os, discord
from discord.ext import commands
from dotenv import load_dotenv

# intents是要求機器人的權限
intents = discord.Intents.all()
# 前缀符号
bot = commands.Bot(command_prefix="/", intents=intents)

# 載入.env檔案
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
print(token)


@bot.event
# 當機器人完成啟動
async def on_ready():
    print(f"当前登录身份 --> {bot.user}")
    botCount = await bot.tree.sync()
    for cmdItem in botCount:
        print(f"sync cmd: {cmdItem.name}")
    

#load commands
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


@bot.command()
async def unload(ctx, extention):
    await bot.unload_extension(f"cogs.{extention}")
    await ctx.send(f"Unloaded {extention} done.")


@bot.command()
async def reload(ctx, extention):
    await bot.reload_extension(f"cogs.{extention}")
    await ctx.send(f"Reloaded {extention} done.")


# 手动刷新命令提示
@bot.command()
async def refreshtree(ctx, extention):
    await bot.tree.sync()


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f'Loaded {filename[:-3]}')
            except Exception as e:
                print(f"Failed to load extension {filename[:-3]}.")
                print(e)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())