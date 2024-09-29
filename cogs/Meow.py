import json
import discord
import requests
import random

from discord import app_commands

from discord.ext import commands

class Meow(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
    
    @app_commands.command(name="meow",description="recommand a cat randomly")
    async def meow(self, interaction: discord.Interaction):        
        with open("resources/data/cat.json", "r") as f:
            cat_data = json.load(f)
            
            idx_random = random.randint(0, len(cat_data)-1)
            item_random = cat_data[idx_random]
            
            item_embed = discord.Embed(title=item_random['name'], color=discord.Color.from_rgb(205,108,61))
            
            # 作者 = PetPal
            # 图标 = PetPal的图标
            img_author_icon = discord.File('img/petpal_logo.png', filename='petpal_logo.png')
            item_embed.set_author(name='PetPal', icon_url='attachment://petpal_logo.png')

            # 循环添加field，每个字段一个field，考虑到字段比较多，inline = True
            # field的标题 = 字段名
            # field的内容 = 字段内容
            item_embed.add_field(name='origin', value=item_random['origin'], inline=True)
            item_embed.add_field(name='length', value=item_random['length'], inline=True)
            item_embed.add_field(name='weight', value=f"{item_random['min_weight']} - {item_random['max_weight']} pounds", inline=True)
            item_embed.add_field(name='life expectancy', value=f"{item_random['min_life_expectancy']} - {item_random['max_life_expectancy']} years", inline=True)
            item_embed.add_field(name='family friendly', value=to_star(item_random['family_friendly']), inline=True)
            item_embed.add_field(name='shedding', value=to_star(item_random['shedding']), inline=True)
            item_embed.add_field(name='general health', value=to_star(item_random['general_health']), inline=True)
            item_embed.add_field(name='playfulness', value=to_star(item_random['playfulness']), inline=True)
            item_embed.add_field(name='meowing', value=to_star(item_random['meowing']), inline=True)
            item_embed.add_field(name='children friendly', value=to_star(item_random['children_friendly']), inline=True)
            item_embed.add_field(name='stranger friendly', value=to_star(item_random['stranger_friendly']), inline=True)
            item_embed.add_field(name='grooming', value=to_star(item_random['grooming']), inline=True)
            item_embed.add_field(name='intelligence', value=to_star(item_random['intelligence']), inline=True)
            item_embed.add_field(name='other pets friendly', value=to_star(item_random['other_pets_friendly']), inline=True)
            
            

            # 添加图片 = 猫的图片            
            img_cat = discord.File(f"img/cats/{item_random['name']}.jpg", filename=f'{item_random['name']}.jpg')            
            item_embed.set_image(url=f'attachment://{item_random['name']}.jpg')

            # 发送Embed消息  
            try: 
                await interaction.response.send_message(files=[img_cat,img_author_icon],embed=item_embed)
            except Exception as e:
                print(f'error: {e}')

            

def to_star(num: int):
    try:
        return  '★' * num + '✰' * (5 - num)
    except Exception as e:
        print(f'error: {e}')
        return  '✰' * 5


async def setup(bot: commands.Bot):
    await bot.add_cog(Meow(bot))
        