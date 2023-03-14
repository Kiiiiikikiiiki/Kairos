import sqlite3
import player, inventory, items, functions
import constant as const
import copy

# Testing if we can construct a database sqlite format for this game
# This file is to test sqlite querries and to learn how to use it properly. 
 

# tuto link : 

# Creating a connection
conn = sqlite3.connect('Kairos/newDB/database.db')

# Creating  the cursor
cur = conn.cursor()

# Executing querries 

# for the player table there is some variables (mostly list and dictionnary variable type) that will have there own table
# and so to retrieve those variable we will need to access to table to that variable and fetch all the rows with the same playerID. 

# Main player table
cur.execute(""" CREATE TABLE IF NOT EXISTS players(
    playerID INT PRIMARY KEY,
    name TEXT,
    money DOUBLE,
    location TEXT,
    guild TEXT,
    active_quest TEXT,
    requirement MEDIUMTEXT
);
""")

# For the inventory of each player we will need to create a new table in another database file (inventory.db) for each player 
# and the name of the table will be the playerID and inside will be all the item the player got. 
# SAME FOR GEARS 
# SAME FOR EQUIPMENTS
# SAME FOR EXPERIENCE

# Sub variable in player data

# Current action var 
# itemRewards and xpRewards will be saved in other database where the table name of each will be the player id
cur.execute(f""" CREATE TABLE IF NOT EXISTS current_action(
    compteur INT PRIMARY KEY,
    playerID INT,
    action TEXT,
    finish_time DATETIME
);
""")

# cur.execute("INSERT INTO players VALUES(?, ?, ?, ?, ?, ?, ?);", [12763713913782734, "test", 34, "testlocation", "solo", "1,2,6", "None"])

cur.execute("SELECT * FROM players;")
result = cur.fetchone()
print(result)

conn.commit()

# No more testing here
folder_before = "Kairos/"

# Constant querries
CREATE_PLAYER = """ CREATE TABLE IF NOT EXISTS players(
    playerID INT PRIMARY KEY,
    name TEXT,
    money DOUBLE,
    location TEXT,
    guild TEXT,
    active_quest TEXT,
    requirement MEDIUMTEXT
);
"""

# Serialisation
def savePlayer(player_list: list[player.Profile]):
    conn = sqlite3.connect(f"{folder_before}newDB/players.db")

    cur = conn.cursor() # Creating the cursor

    # Delete the current table of players so that we can re-populate it
    cur.execute("""DROP TABLE IF EXISTS players
    """)

    # Re-creatre the table
    cur.execute(CREATE_PLAYER)

    # Re-populate the player database
    for p in player_list:
        activeQuest = ','.join(p.active_quest) # Listing the active quest in a string to save the data
        requirements = ','.join(p.requirement) # Listing the requirements in a string to save the data
        cur.execute("INSERT INTO players VALUES(?, ?, ?, ?, ?, ?, ?);", [p.profile_id, p.name, p.money, p.location,
                                                                          p.guild, activeQuest, requirements])
    
    conn.commit()


def saveInventory(player_list: list[player.Profile]):
    conn = sqlite3.connect(f"{folder_before}newDB/inventories.db") # Connecting to db

    cur = conn.cursor() # Creating the curso

    for p in player_list:
        # Delete table if player had already saved before
        cur.execute(f"""DROP TABLE IF EXISTS {p.profile_id}""")

        # Re-create the table to re-populate it 
        cur.execute(f""" CREATE TABLE {p.profile_id}(
        itemID TEXT PRIMARY KEY,
        condition TEXT,
        nb INT
        modifier TEXT
        );""")

        # Insert new data in their respective table
        duplicate = []
        itemsTuple = list(map(lambda x: (x.item_id, x.condition), p.inventory.inv)) # List of the items with their id and their condition
        for item in p.inventory.inv:
            if (item.item_id, item.condition) not in duplicate:
                nb = itemsTuple.count((item.item_id, item.condition)) # Number of occurence the player as this item 
                cur.execute(f"INSERT INTO {p.profile_id} VALUES(?, ?, ?, ?);", [item.item_id, item.condition, nb, None])
                duplicate.append((item.item_id, item.condition))




# Deserialisation
def loadPlayer():
    conn = sqlite3.connect(f"{folder_before}newDB/players.db")

    cur = conn.cursor() # Creating the cursor

    # Get a list of all the players data
    cur.execute("SELECT * FROM players;")
    #TODO Here we select from all the other database that we have to create for the other parameters in player 
    players_list = cur.fetchall()

    #TODO in this loop, we will get all the select fetchall() result and create the new player class that will corespond to that player
    #       and then put it in const.PLAYER_DICT so we can access it in the main code. 
    for p in players_list:
        new_player = player.Profile()


def loadInventory(profile_id: str):
    conn = sqlite3.connect(f"{folder_before}newDB/inventories.db")

    cur = conn.cursor()

    cur.execute(f"IF EXISTS SELECT * FROM {profile_id};")

    inv = cur.fetchall()

    new_inv = inventory.Inventory()
    for item in inv:
        # Make new function that take an sql item to the item object
        pass



# Funtions to help serialisation and deserialisation

def sqlItems_to_object(sqlItems: list):
    itemList : list[items.Item] = []

    for i in sqlItems:
        item: items.Item = functions.getItem(i[0])  # Get the base item for the id provided

        item.condition = i[1]   # Get the condition of the item

        # TODO must add the code here to retrieve modifiers and applied them to item

        # TODO have to modify the way item are added to inventory. Now we sould save item by tuple or by adding a nb parameter to item class
        for r in range(i[2]): 
            itemList.append(item)
