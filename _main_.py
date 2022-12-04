from datetime import datetime
import sys
import traceback
import discord
import discord.ext.commands
import discord.ext.tasks
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option
from discord.ui import Button, View
from dotenv import dotenv_values
from discord import Embed, Interaction, OptionChoice, User
import embeds
import player
import pockethouse
import incubator
import items
import inventory
import functions
import gears
import job
import constant as const
from db import db_func
import copy
import checks

bot = discord.Bot()

config = dotenv_values(".env")

# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/ BOT EVENTS /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*


@bot.event
async def on_ready():
    channel = bot.get_channel(933532273825968242)
    # Here we deserialize everything that need to be put in constant
    db_func.deserialize_profile()
    # Up and running baby
    await channel.send('***Kairos is Up and Running!***')


@bot.event
async def on_disconnect():
    db_func.save_profile(list(const.PROFILE_DICT.values()))
    db_func.save_phouse(list(const.PROFILE_DICT.values()))
    db_func.save_guild(const.GUILD_LIST)  # need to change fo dict


@bot.event  # **THIS NEED TO BE TESTED**
async def on_member_join(member: discord.Member):
    newProfile = player.Profile(member.name, member.id)
    const.PROFILE_DICT[f'{member.id}'] = newProfile


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, discord.errors.CheckFailure):
        pass
    else:
        raise error

# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/ BOT CHECKS /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
def is_guild_admin():
    async def predicate(ctx):
        if ctx.author.id not in [221689857985085440]:
            await ctx.respond(f"You can't do that **{ctx.author.name}**", ephemeral=True)
        return ctx.author.id in [221689857985085440]
    return commands.check(predicate)


def has_gears_on_him(ctx):
    plyer: player.Profile = const.PROFILE_DICT[f"{ctx.author.id}"]
    cpt = 0
    for i in plyer.getGears():
        if i != f"{items.noneItem.name}":
            cpt += 1
    return cpt != 0


def has_gears_in_inv(ctx):
    plyer: player.Profile = const.PROFILE_DICT[f"{ctx.author.id}"]
    return len(plyer.getGearsInInv()) != 0


def has_equip_in_inv(ctx):
    plyer: player.Profile = const.PROFILE_DICT[f"{ctx.author.id}"]
    return len(plyer.getEquipmentInInv()) != 0


def has_equip_on_him(ctx):
    plyer: player.Profile = const.PROFILE_DICT[f"{ctx.author.id}"]
    cpt = 0
    for i in plyer.getEquipments():
        if i != f"{items.noneItem.name}":
            cpt += 1
    return cpt != 0

# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/ BOT COMMANDS /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*


# /*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/ TEST AREA /*/*/*/*/*/*/*/*/*/*/*/
@bot.slash_command(guild_ids=[933532273825968239])
async def type_v(ctx):
    await ctx.respond(f"{type(discord.Colour(0xff0000))}")
    plyer: player.Profile = const.PROFILE_DICT[f'{ctx.author.id}']
    plyer.inventory.inv.append(const.ITEMS_DICT['0001'])
    plyer.inventory.inv.append(const.ITEMS_DICT['0002'])
    plyer.inventory.inv.append(const.ITEMS_DICT['0002'])
    plyer.inventory.inv.append(const.ITEMS_DICT['0003'])
    plyer.inventory.inv.append(const.ITEMS_DICT['0003'])
    plyer.inventory.inv.append(const.ITEMS_DICT['0003'])
    plyer.inventory.inv.append(functions.getItem("0010"))


@bot.slash_command(guild_ids=[933532273825968239], description="This is a test")
@checks.check_doing_something()
async def test(ctx):
    await ctx.respond(embed=embeds.levelUp_embed(player_name="TestName", skill_name="mining", skill_emoji="⛏️", new_lvl=1))
    # await job.testMine.enter(ctx=ctx, equipment=const.PROFILE_DICT[f"{ctx.author.id}"].p_equipment, player=const.PROFILE_DICT[f"{ctx.author.id}"])
    # await ctx.delete()  # delete make it that we dont need a respond


# /*/*///*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*/ REAL COMMAND AREA /*/*/*/*/*/*/*/*/


# /*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
# /*/*/*/*/*/ Admins Command /*/*/*/*/*/*/*/*/*/*/*/
@bot.slash_command(name="close", guild_ids=[933532273825968239], description="Close the bot")
@is_guild_admin()
async def botclose(ctx):
    await bot.close()


@bot.slash_command(name="give", guild_ids=[933532273825968239], descripion="give an item to a player")
@is_guild_admin()
async def give(ctx, user: discord.User, item_id: str):
    finalEmbed, view = functions.receiveItems(user.id, [copy.deepcopy(
        const.ITEMS_DICT[f'{item_id}'])], const.PROFILE_DICT[f'{user.id}'], ctx=ctx)
    await user.send(embed=finalEmbed, view=view)
    await ctx.delete()

# /*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
# /*/*/*/*/*/ Guild Group Command /*/*/*/*/*/*/*/*/*/*/*/

clan = SlashCommandGroup(
    "guild", "Everything to manage and interact with your guild")


@clan.command(name='create', guild_ids=[933532273825968239], description="Create your own guild")
async def create_guild(ctx,
                       guild_name: Option(str, description="Name of your guild"),
                       guild_color: Option(str,
                                           description="Color of your guild",
                                           choices=const.COLOR_CHOICES),
                       guild_private: Option(bool, description="If your guild is private")):
    # HEX CODE for the color choice
    hex_gcolor: str = const.HEX_BY_COLOR_NAME[guild_color]
    # Convert HEX color code to int value
    Gcolor_int = int(("0x" + (hex_gcolor.replace("#", ""))), base=16)
    founder = ctx.author
    await ctx.respond(embed=embeds.simple_reponse(f"Guild **{guild_name}** created successfully!"))


# /*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
# /*/*/*/*/* Inv Group Command /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/

inv = SlashCommandGroup(
    "inv", "Everything to manage and interact with your inventory")


@inv.command(name='see', guild_ids=[933532273825968239], description="Check your inventory")
async def see_inv(ctx):
    plyer: player.Profile = const.PROFILE_DICT[f'{ctx.author.id}']
    # Receive the items and usables items in a custom string to be displayed
    itemsStr, usableItemStr = functions.getItemsFromInv(plyer.profile_id)

    invEmbed = Embed(title=f">>> {plyer.name} | Inventory")
    invEmbed.add_field(name="**Items**", value=itemsStr)
    invEmbed.add_field(name="**Usables**", value=usableItemStr, inline=True)
    invEmbed.set_thumbnail(url=ctx.author.avatar)
    invEmbed.set_footer(
        text=f"|💲money: {plyer.money} | 🗾Location: {plyer.location} | 🔱Guild: {plyer.guild} |")
    await ctx.respond(embed=invEmbed)


# /*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*
# /*/*/*/*/* Profile Command /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
class EmbedButton(Button):
    def __init__(self, label, embed: Embed, ctx: discord.ext.commands.Context):
        super().__init__(style=discord.ButtonStyle.green, label=label)
        self.embed = embed
        self.ctx = ctx

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.ctx.author.id:
            await interaction.response.edit_message(embed=self.embed)


class ProfileView(View):
    def __init__(self, timeout: float = 180):
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        self.stop()
        print("TIMEOUT!!")


@bot.slash_command(name="profile", guild_ids=[933532273825968239], description="Check your profile")
async def see_profile(ctx):
    plyer: player.Profile = const.PROFILE_DICT[f'{ctx.author.id}']
    profileEmbed = embeds.getProfileEmbed(ctx, plyer)

    # Create button that are added at the end of the embed so player can navigate between multiple "screen"
    buttonProfile = EmbedButton("Profile", embed=profileEmbed, ctx=ctx)
    buttonEquipment = EmbedButton(
        "Equipment", embed=embeds.getEquipmentEmbed(ctx, plyer), ctx=ctx)
    buttonVirtues = EmbedButton("Virtues", embeds.simple_reponse(
        "Still need top make an embed for that(Virtues)"), ctx)
    buttonGems = EmbedButton("Gems", embeds.simple_reponse(
        "Still need top make an embed for that(Gems)"), ctx)
    buttonArtifacts = EmbedButton("Artifacts", embeds.simple_reponse(
        "Still need top make an embed for that(Artifacts)"), ctx)
    buttonSkill = EmbedButton("Skills", embed=embeds.skillsEmbed(ctx=ctx, player=plyer), ctx=ctx)

    # Create the view where all the buttons are added 
    view = ProfileView()
    view.add_item(buttonProfile)
    view.add_item(buttonEquipment)
    view.add_item(buttonVirtues)
    view.add_item(buttonGems)
    view.add_item(buttonArtifacts)
    view.add_item(buttonSkill)

    await ctx.respond(embed=profileEmbed, view=view)


@bot.slash_command(name="gears", guild_ids=[933532273825968239], description="Interact with your gears")
async def gearsInteraction(ctx,
                           action: Option(str, "the action to do", choices=["equip", "remove"])):
    isRemove = True
    if action == "equip":
        isRemove = False

    # Check Time
    checkPass = True
    if isRemove:
        if not has_gears_on_him(ctx=ctx):
            checkPass = False
            await ctx.respond("**You dont have any gears on you!**", ephemeral=True)
    else:
        if not has_gears_in_inv(ctx=ctx):
            checkPass = False
            await ctx.respond("**You dont have any gears in your inventory!**", ephemeral=True)

    if checkPass:
        view = functions.Equipment_Gears_Action(
            plyer=const.PROFILE_DICT[f'{ctx.author.id}'], ctx=ctx, isGears=True, isRemove=isRemove)
        await ctx.respond("This is a test for a dropdown", view=view, ephemeral=True)


@bot.slash_command(name="equipments", guild_ids=[933532273825968239], description="Interact with your equipments")
async def equipmentsInteraction(ctx,
                                action: Option(str, "the action to do", choices=["equip", "remove"])):
    isRemove = True
    if action == "equip":
        isRemove = False

    # Check Time 
    checkPass = True 
    if isRemove:
        if not has_equip_on_him(ctx=ctx):
            checkPass = False
            await ctx.respond("**You dont have any equipment on you!**", ephemeral=True)
    else:
        if not has_equip_in_inv(ctx=ctx):
            checkPass = False
            await ctx.respond("**You dont have any equipments in your inventory!**", ephemeral=True)

    if checkPass:
        view = functions.Equipment_Gears_Action(
            plyer=const.PROFILE_DICT[f'{ctx.author.id}'], ctx=ctx, isGears=False, isRemove=isRemove)
        await ctx.respond("This is a test for a dropdown", view=view, ephemeral=True)


@bot.slash_command(name="me", guild_ids=[933532273825968239], description="Know what you are currently doing")
async def whatThePlayerIsDoing(ctx):
    plyer: player.Profile = const.PROFILE_DICT[f'{ctx.author.id}']
    # If the player action will reward him with rewards
    as_reward = plyer.current_Action["rewards"] is not None
    # If the player is actually doing something that can be cancel
    as_action = plyer.current_Action["action"] != "None"

    # if the player is done with is action and doesn't have a reward then reset it to doing nothing
    if as_action:
        if plyer.is_action_done():
            as_action = False
    
    await ctx.respond(embed=embeds.getCurrentActionEmbed(ctx=ctx, action=plyer.current_Action["action"], time_until_ready=plyer.current_Action["finish_time"],
                                                         player_name=plyer.name),
                      view=functions.getCurrentActionView(as_reward=as_reward, as_action=as_action, player=plyer))
# /*/*//*/*/*/*/*/* CODE TEST /*/*//*/*/**/*///*


bot.add_application_command(clan)
bot.add_application_command(inv)

bot.run(config['token'])
