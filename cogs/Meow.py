import json,discord,random

from discord import app_commands
from discord.ext import commands
from discord.app_commands.models import Choice
from typing import Optional

class Meow(commands.Cog):
    
    # properties
    lst_cat = []
    lst_origin = []

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        # 用cat.json文件初始化orgin列表
        with open("resources/data/cat.json", "r") as f:
            self.lst_cat = json.load(f)
            self.lst_origin = [Choice(name=item['origin'], value=item['origin']) for item in self.lst_cat]
                

    # random cat
    @app_commands.command(name="meow", description="recommand a cat randomly")
    async def meow(self, interaction: discord.Interaction):       
        idx_random = random.randint(0, len(self.lst_cat) - 1)
        item_random = self.lst_cat[idx_random]
        
        item_embed, img_cat, img_author_icon = self.create_cat_embed(item_random)

        # 发送Embed消息  
        try: 
            await interaction.response.send_message(files=[img_cat, img_author_icon], embed=item_embed)
        except Exception as e:
            print(f'error: {e}')

    # cat by condition
    @app_commands.command(name="meow_by_condition", description="recommand a cat by condition")
    @app_commands.choices(
        weight_range=[
            Choice(name="light", value=1),
            Choice(name="medium", value=2),
            Choice(name="heavy", value=3)
        ],
        family_friendly=[
            Choice(name="must be", value=5),
            Choice(name="nice to have", value=3),
            Choice(name="not important", value=1)
        ],
        shedding_tolerance=[
            Choice(name="allergic to it", value=1),
            Choice(name="acceptable", value=3),
            Choice(name="totally no problem", value=5)
        ],
        playfulness=[
            Choice(name="not playful", value=1),
            Choice(name="normal", value=3),
            Choice(name="very playful", value=5)
        ],
        meowing=[
            Choice(name="quiet", value=1),
            Choice(name="normal", value=3),
            Choice(name="noisy", value=5)
        ],
        children_friendly=[
            Choice(name="not important", value=1),
            Choice(name="nice to have", value=3),
            Choice(name="must be", value=5)
        ],
        stranger_friendly=[
            Choice(name="not important", value=1),
            Choice(name="nice to have", value=3),
            Choice(name="must be", value=5)
        ],
        grooming=[
            Choice(name="not important", value=1),
            Choice(name="nice to have", value=3),
            Choice(name="must be", value=5)
        ],
        intelligence=[
            Choice(name="not important", value=1),
            Choice(name="not stupid", value=3),
            Choice(name="clever", value=5)
        ],
        other_pets_friendly=[
            Choice(name="not important", value=1),
            Choice(name="nice to have", value=3),
            Choice(name="must be", value=5)
        ]
    )
    async def meow_by_condition(
        self, 
        interaction: discord.Interaction, 
        origin: Optional[str] = None,  # 原产国，通过自动完成获取
        weight_range: Optional[Choice[int]] = None, # 体重范围，通过选择获取，1=light, 2=medium, 3=heavy
        family_friendly: Optional[Choice[int]] = None, # 家庭友好度，通过选择获取，1=not important, 3=nice to have, 5=must be
        shedding_tolerance: Optional[Choice[int]] = None, # 脱毛耐受度，通过选择获取，1=allergic to it, 3=acceptable, 5=totally no problem
        playfulness: Optional[Choice[int]] = None, # 游戏性，通过选择获取，1=not playful, 3=normal, 5=very playful
        meowing: Optional[Choice[int]] = None,  # 喵叫声，通过选择获取，1=quiet, 3=normal, 5=noisy
        children_friendly: Optional[Choice[int]] = None,  # 对小孩友好度，通过选择获取，1=not important, 3=nice to have, 5=must be
        stranger_friendly: Optional[Choice[int]] = None,  # 对陌生人友好度，通过选择获取，1=not important, 3=nice to have, 5=must be
        grooming: Optional[Choice[int]] = None,  # 美容度，通过选择获取，1=not important, 3=nice to have, 5=must be
        intelligence: Optional[Choice[int]] = None, # 智商，通过选择获取，1=not important, 3=not stupid, 5=clever
        other_pets_friendly: Optional[Choice[int]] = None # 对其他宠物友好度，通过选择获取，1=not important, 3=nice to have, 5=must be
    ):
        try:
            # 根据条件筛选猫  
            # 根据max_weight字段对lst_cat进行排序
            lst_cat_sorted = sorted(self.lst_cat, key=lambda x: x['max_weight'])
            lst_cat_filtered = []
            # 根据体重范围筛选,这里其实只关注最大重量，用户其实关注的也是这个而不是最小体重
            # 如果weight_range = 1, 则筛选列表中的前27个猫
            # 如果weight_range = 2, 则筛选列表中的中间27个猫
            # 如果weight_range = 3, 则筛选列表中的后27个猫
            if weight_range == None:
                lst_cat_filtered = lst_cat_sorted
            else:
                print(weight_range.value)
                if weight_range.value == 1: 
                    lst_cat_filtered = lst_cat_sorted[:27]
                elif weight_range.value == 2:
                    lst_cat_filtered = lst_cat_sorted[27:54]
                elif weight_range.value == 3:
                    lst_cat_filtered = lst_cat_sorted[54:]

            # 根据family_friendly筛选，直接筛选lst_cat_filtered中的family_friendly字段大于等于family_friendly.value的猫
            if family_friendly != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'family_friendly' in item and item['family_friendly'] >= family_friendly.value]
            
            # 根据shedding_tolerance筛选，直接筛选lst_cat_filtered中的shedding字段小于等于shedding_tolerance.value的猫
            if shedding_tolerance != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'shedding' in item and item['shedding'] <= shedding_tolerance.value]

            # 根据playfulness筛选，直接筛选lst_cat_filtered中的playfulness字段在playfulness.value-1到playfulness.value+1之间的猫
            if playfulness != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'playfulness' in item and item['playfulness'] >= playfulness.value - 1 and item['playfulness'] <= playfulness.value + 1]
            
            # 根据meowing筛选，直接筛选lst_cat_filtered中的meowing字段在meowing.value-1到meowing.value+1之间的猫
            if meowing != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'meowing' in item and item['meowing'] >= meowing.value - 1 and item['meowing'] <= meowing.value + 1]
            
            # 根据children_friendly筛选，直接筛选lst_cat_filtered中的children_friendly字段大于等于children_friendly.value的猫
            if children_friendly != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'children_friendly' in item and item['children_friendly'] >= children_friendly.value]

            # 根据stranger_friendly筛选，直接筛选lst_cat_filtered中的stranger_friendly字段大于等于stranger_friendly.value的猫
            if stranger_friendly != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'stranger_friendly' in item and item['stranger_friendly'] >= stranger_friendly.value]
            
            # 根据grooming筛选，直接筛选lst_cat_filtered中的grooming字段大于等于grooming.value的猫
            if grooming != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'grooming' in item and item['grooming'] >= grooming.value]

            # 根据intelligence筛选，直接筛选lst_cat_filtered中的intelligence字段大于等于intelligence.value的猫
            if intelligence != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'intelligence' in item and item['intelligence'] >= intelligence.value]
            
            # 根据other_pets_friendly筛选，直接筛选lst_cat_filtered中的other_pets_friendly字段大于等于other_pets_friendly.value的猫
            if other_pets_friendly != None and len(lst_cat_filtered) > 0:
                lst_cat_filtered = [item for item in lst_cat_filtered if 'other_pets_friendly' in item and item['other_pets_friendly'] >= other_pets_friendly.value]

            if len(lst_cat_filtered) == 0:
                await interaction.response.send_message("no cat found")
                return
            else:
                idx_random = random.randint(0, len(lst_cat_filtered) - 1)
                item_random = lst_cat_filtered[idx_random]
                item_embed, img_cat, img_author_icon = self.create_cat_embed(item_random)
                await interaction.response.send_message(files=[img_cat, img_author_icon], embed=item_embed)
        except Exception as e:
            print(f'error: {e}')

    @meow_by_condition.autocomplete('origin')
    async def autocomplete_origin(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=origin.name, value=origin.value) for origin in self.lst_origin if current.lower() in origin.name.lower()]

    # cat by name
    @app_commands.command(name="meow_by_name", description="search cat by name")
    async def meow_by_name(self, interaction: discord.Interaction, name: str):
        try:
            res_cat = [item for item in self.lst_cat if name.lower() in item['name'].lower()]
            if len(res_cat) == 0:
                await interaction.response.send_message("no cat found")
                return
            item_random = res_cat[0]
            item_embed, img_cat, img_author_icon = self.create_cat_embed(item_random)
            await interaction.response.send_message(files=[img_cat, img_author_icon], embed=item_embed)
            
        except Exception as e:
            print(f'error: {e}')
    
    @meow_by_name.autocomplete('name')
    async def autocomplete_name(self, interaction: discord.Interaction, current: str):
        return [app_commands.Choice(name=item['name'], value=item['name']) for item in self.lst_cat if current.lower() in item['name'].lower()]

    # create cat embed
    def create_cat_embed(self, item_random):
        # 创建Embed消息
        item_embed = discord.Embed(title=item_random['name'], color=discord.Color.from_rgb(205, 108, 61))
        
        # 作者 = PetPal
        # 图标 = PetPal的图标
        img_author_icon = discord.File('img/petpal_logo.png', filename='petpal_logo.png')
        item_embed.set_author(name='PetPal', icon_url='attachment://petpal_logo.png')

        # 循环添加field，每个字段一个field，考虑到字段比较多，inline = True
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

        return item_embed, img_cat, img_author_icon

def to_star(num: int):
    try:
        return '★' * num + '✰' * (5 - num)
    except Exception as e:
        print(f'error: {e}')
        return '✰' * 5

async def setup(bot: commands.Bot):
    await bot.add_cog(Meow(bot))