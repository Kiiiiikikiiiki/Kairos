from player import Profile 
from discord.ext import commands
from constant import PROFILE_DICT



def check_doing_something():
    '''
    Check if a player is currently doing something
    Return True if doing something or hasn't collected is reward yet
    Return False if is doing nothing
    '''

    async def predicate(ctx):
        player = PROFILE_DICT[f'{ctx.author.id}']
        if player.current_Action.get("action") != "None":
            if player.is_action_done():
                return True
            await ctx.respond(f"You can't do that while doing {player.current_Action.get('action')}", ephemeral=True)
            return False
        else:
            return True
    return commands.check(predicate)
            
