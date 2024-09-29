import discord,os
from dotenv import load_dotenv
import requests
import random

from discord import app_commands

from discord.ext import commands

class Meow(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()

    @app_commands.command(name="meow",description="recommand a cat randomly")
<<<<<<< HEAD
    async def meow(self, interaction: discord.Interaction):

        load_dotenv()
        ninjia_key = os.getenv("X_Api_Key")
        offset_random = random.randint(0, 81)

        query_string = f'min_weight=1&offset={offset_random}'
        res = requests.get(f"https://api.api-ninjas.com/v1/cats?{query_string}", headers={'X-Api-Key':f'{ninjia_key}'})
        print(res.json())
        if res.status_code == 200:            
            idx_random = random.randint(0, len(res.json())-1)

            item_random = res.json()[idx_random]


            print(f'item_random[name]={item_random["name"]}')
            # 初始化Embed，其中：
            # 标题 = 猫名
            # 颜色 = PetPal的主题色
=======
    async def meow(self, interaction: discord.Interaction):        
        with open("resources/data/cat.json", "r") as f:
            cat_data = json.load(f)
            print(f'cat_data: {cat_data}')
            idx_random = random.randint(0, len(cat_data)-1)
            item_random = cat_data[idx_random]
            
>>>>>>> parent of 693ab7e (localize the cat img resources)
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

<<<<<<< HEAD


=======
>>>>>>> parent of 693ab7e (localize the cat img resources)
            # 添加图片 = 猫的图片
            item_embed.set_image(url=item_random['image_link'])
            print(item_random)
            print(f'item_embed: {item_embed}')                       
            try: 
                await interaction.response.send_message(file=img_author_icon,embed=item_embed)
            except Exception as e:
                print(f'error: {e}')
        else:
            await interaction.response.send_message(f'something is wrong')


def to_star(num: int):
    try:
        return  '★' * num + '✰' * (5 - num)
    except Exception as e:
        print(f'error: {e}')
        return  '✰' * 5


async def setup(bot: commands.Bot):
    await bot.add_cog(Meow(bot))