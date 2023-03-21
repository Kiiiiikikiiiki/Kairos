from datetime import datetime



class CurrentAction:
    def __init__(self, actionName: str = None, finishTime: datetime = None, itemReward: list[dict] = None, xpReward: list[tuple] = None, 
                 moneyReward: int = None, requirementReward: list[str] = None):
        '''
        Parameters
        ----------
        actionName        : String 
            The name of the action the player is doing

        finishTime        : datetime including months, days, hours, minutes, seconds
            The time at which the action is done doing. Can be None if there is no definite time

        itemReward        : List of dict of item : {'item': Item, 'nb': int}
        xpReward          : List of tuple : (number of xp (int), type of xp (string))
        moneyReward       : int 
        requirementReward : List of string 
            if the player was required to do this action at the end of it will receive the requirement.      
        '''

        self.actionName        = actionName
        self.finishTime        = finishTime
        self.itemReward        = itemReward
        self.xpReward          = xpReward
        self.moneyReward       = moneyReward
        self.requirementReward = requirementReward

    
    def reset(self):
        pass