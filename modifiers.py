class XpMultiplier:
    '''
    Will give a define multiplier to a xp rewards
    '''

    def __init__(self, multiplier: float, xpType: list[str]):
        self.multiplier = multiplier
        self.xpType = xpType
    

    def apply(self, **kwargs):
        if 'xp_reward' and 'xpType' in kwargs.keys() and kwargs.get('xpType') in self.xpType:
            return kwargs.get('xp_reward') + (kwargs.get('xp_reward') * self.multiplier)


class MoneyMultiplier:
    '''
    Will give a define multiplier to a money rewards
    '''

    def __init__(self, multiplier: float):
        self.multiplier = multiplier

    
    def apply(self, **kwargs):
        if 'money_reward' in kwargs.keys():
            return kwargs.get('money_reward') + (kwargs.get('money_reward') * self.multiplier)


class Modifiers:
    def __init__(self, modifierClass: any):
        self.modifierClass = modifierClass

    
    def apply(self, **kwargs):
        return self.modifierClass.apply(**kwargs)



##################################################################################################
####################################### TESTING ZONE #############################################
##################################################################################################
test1 = Modifiers(modifierClass=XpMultiplier(0.5, ['mining']))
test2 = Modifiers(modifierClass=MoneyMultiplier(-0.25))
printer = test1.apply(test=5)
 

money=500
xp=100
varList: list = [money, xp]
cpt = 0
for modifier in [test1, test2]:
    varList[cpt] = modifier.apply(xp_reward=xp, money_reward=money, test=60, xpType='mining')
    cpt += 1

money, xp = varList

print(money, xp)
