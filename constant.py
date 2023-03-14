import playerFiles.player
import guild
import items


# /*/*/*/*/*/*/*/**/*/*/ GUILD CONSTANTE /*/*/*//*/*/*/*/*/*/*/*/*/*/*/**//*/*/*/
COLOR_CHOICES = ["Royal Blue", "Malibu", "Curious Blue", "Blizzard Blue", "Aqua", "Guardsman Red", "Scarlet", "Tall Poppy", "French Rose", "Fuchsia",
                 "Lime", "Apple", "Sushi", "Camarone", "Galliano", "Gold", "Gunsmoke", "Hot Cinnamon", "Las Palmas", "White", "Black"]

HEX_BY_COLOR_NAME = {
    "Royal Blue": "#3E78DA",
    "Malibu": "#81D4FA",
    "Curious Blue": "#1E88E5",
    "Blizzard Blue": "#B2EBF2",
    "Aqua": "#00FFFF",
    "Guardsman Red": "#CC0000",
    "Scarlet": "#FF3300",
    "Tall Poppy": "#C62828",
    "French Rose": "#EC407A",
    "Fuchsia": "##FF00FF",
    "Lime": "#00FF00",
    "Apple": "#388E3C",
    "Sushi": "#7CB342",
    "Camarone": "#006600",
    "Galliano": "#D4AC0D",
    "Gold": "#FFD700",
    "Gunsmoke": "#828685",
    "Hot Cinnamon": "#D2691E",
    "Las Palmas": "#C6E610",
    "White": "#FFFFFF",
    "Black": "#000000",
}


# /*/*/*/*//*/*/*/*/*/*/*/* BIG DATA LIST TO FILL UP AT START /*/**/*/*/*/*/*/*/**/*/*/*/*/
PROFILE_LIST: list[playerFiles.player.Profile] = []
PROFILE_DICT: dict = {}

GUILD_LIST: list[guild.guild] = []

# /*/*/*/*//*/*/*/*/*/*/*/* Others /*/**/*/*/*/*/*/*/**/*/*/*/*/
URL = "https://www.google.com/"

# */*/*/*/*/*//*/*/*/*/*/*/*/ SKILLS SAVING DATA /*/*/*/*/*/*/*/
LVL = "lvl"
CURRENT_EXP = "current_exp"
NEXT_LVL_EXP = "next_lvl_exp"

# /*/*/*/*/*/*/*/*/*/*/*/*/ ALL ITEMS /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/
ITEMS_DICT: dict = {
    "0000": items.noneItem,
    "0001": items.test1,
    "0002": items.test2,
    "0003": items.test3,
    "0004": items.test4,
    "0005": items.test5,
    "0006": items.test6,
    "0007": items.test7,
    "0008": items.test8,
    "0009": items.test9,
    "0010": items.test10,
    "0011": items.test11,
    "0012": items.test12,
    "0013": items.test13,
    "0014": items.test14,
    "0015": items.test15,
    "0016": items.test16
}
