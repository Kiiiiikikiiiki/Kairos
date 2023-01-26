from datetime import datetime
import profile
from re import L
from unicodedata import name
from discord import Embed
import discord
import discord.ext.commands
import functions
from items import Item
from player import Profile


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /*/*/*/*/*/*/*/*/*/ SIMPLE RESPONSE EMBED FUNCTON /*/*/*/*/

def simple_reponse(response: str):
    embed_ = Embed(title=f'{response}')
    return embed_


# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /*/*/*/*/*/*/*/*/*/ PROFILE EMBED /*/*/*/*/
def getProfileEmbed(ctx: discord.ext.commands.Context, profile: Profile):
    profileEmbed = Embed(title=f">>> {profile.name} | Profile")

    profileEmbed.add_field(name="**GEARS**", value=f"**🎩Hat**\n{profile.p_gears.hat.display()}\n\n**👕Chestpiece**\n{profile.p_gears.chestpiece.display()}\n\n**🩳Legspants**\n{profile.p_gears.legspants.display()}\n\n**🧤Gloves**\n{profile.p_gears.gloves.display()}\n\n**📿Necklace**\n{profile.p_gears.necklace.display()}\n\n**💍Ring 1**\n{profile.p_gears.ring1.display()}\n\n**💍Ring 2**\n{profile.p_gears.ring2.display()}")
    profileEmbed.add_field(name="**INFO**", value="**⭐Level**\n4\n\n**✍Title**\nDummy Of The Year\n\n**🔱Guild**\nSolo-Player\n\n**💲Money**\n20000\n\n**🗺Location**\nEtherCity\n\n**🛖Pocket House**\nLevel 1", inline=True)
    profileEmbed.add_field(name="**STATS**", value="**⚔️Atk. Power**\n134\n\n**🪄Magic Atk. Power**\n785\n\n**❤Max HP**\n12450", inline=True)
    profileEmbed.set_thumbnail(url=ctx.author.avatar)

    return profileEmbed


def getEquipmentEmbed(ctx: discord.ext.commands.Context, profile: Profile):
    equipmentEmbed = Embed(title=f">>> {profile.name} | Equipment")

    equipmentEmbed.add_field(name="🗡Weapon", value=f"{profile.p_equipment.weapon.display()}")
    equipmentEmbed.add_field(name="⛏Pickaxe", value=f"{profile.p_equipment.pickaxe.display()}", inline=True)
    equipmentEmbed.add_field(name="🪓Axe", value=f"{profile.p_equipment.axe.display()}", inline=True)
    equipmentEmbed.add_field(name="🎣Fishing rod", value=f"{profile.p_equipment.fishing_rod.display()}")
    equipmentEmbed.add_field(name="☭Scythe", value=f"{profile.p_equipment.scythe.display()}", inline=True)
    equipmentEmbed.add_field(name="🔪Knife", value=f"{profile.p_equipment.knife.display()}", inline=True)
    equipmentEmbed.add_field(name="🪛Lockpick", value=f"{profile.p_equipment.lockpick.display()}")
    equipmentEmbed.add_field(name="🔨Forge Hammer", value=f"{profile.p_equipment.forge_hammer.display()}", inline=True)
    # need 1 more maybe ?
    equipmentEmbed.set_thumbnail(url=ctx.author.avatar)

    return equipmentEmbed
    

def skillsEmbed(ctx: discord.ext.commands.Context, player: Profile):
    embed = Embed(title=f">>> {player.name} | Skills")
    embed.set_thumbnail(url=ctx.author.avatar)

    # skill = player.experience.skills.get(player.experience.PLAYER_XP_TYPE)
    # progress = functions.skillProgress(current_exp=skill['current_exp'], next_levl_exp=skill['next_lvl_exp'])

    # embed.add_field(name="🙋🏻‍♂️Player", value=f"Level {skill['lvl']}\n" + 
    #                                         f"`{skill['current_exp']} / {skill['next_lvl_exp']}`\n" +
    #                                         f"{progress}")
    
    for sk_name, sk in player.experience.skills.items():
        progress = functions.skillProgress(current_exp=sk['current_exp'], next_levl_exp=sk['next_lvl_exp'])

        embed.add_field(name=f"{sk_name}", value=f"Level {sk['lvl']}\n" + 
                                            f"`{sk['current_exp']} / {sk['next_lvl_exp']}`\n" +
                                            f"{progress}")


    return embed


def getMineEmbed(ctx: discord.ext.commands.Context, profile: Profile, mineName: str, mineDesc: str, mineLoot: list[Item]):
    # Making the string with all the possible loot
    loot: str = ""
    for i in mineLoot:
        loot += f"`{i.name}`" + "\n"

    embed = Embed(title=f">>> {mineName}", description=f"{mineDesc}")
    embed.add_field(name="Your pickaxe", value=f"➡ {profile.p_equipment.pickaxe.display()}\n")
    embed.add_field(name="Possible loot", value=loot, inline=False)

    return embed


def getCurrentActionEmbed(ctx: discord.ext.commands.Context, action: str, time_until_ready: datetime, player_name: str):
    if action != "None":
        embed = Embed(title=f">>> {player_name}", description=f"You are currently {action}")
        embed.add_field(name="Time until completion", value=f"⌛`{str(functions.get_timeUntilReady(time_until_ready))[:-7]}`") # remove miliseconds
    else:
        embed = Embed(title=f">>> {player_name}", description="You are currently not doing anything.")

    return embed


def missingPlaceInInv_Embed(missing_slot: int):
    embed = Embed(title="Not enough space in your inventory!")
    embed.add_field(name="Missing slot", value=missing_slot)
    embed.set_footer(text="TIPS: *delete items from your inventory* | *Store some items in one of your storage place*")
    return embed


def levelUp_embed(player_name: str, skill_name: str, skill_emoji: str, new_lvl: int):
    embed = Embed(title="🔺LEVEL UP🔺", description=f"`{player_name}` has gain `1` level in `{skill_emoji}{skill_name}`")
    embed.add_field(name=f"**{skill_emoji}**{skill_name.upper()}", value=f"__Level__ **{new_lvl - 1}** ➡ __Level__ **{new_lvl}**")

    return embed


def locationEmbed(name: str, description: str):
    embed = Embed(title=name, description=description)
    return embed
