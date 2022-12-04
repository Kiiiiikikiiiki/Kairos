class guild:

    ranks = ['Founder',     # All perms
             'Consultant',  # Can manage guild base and kick people from guild
             'High Rank',   # Can deposit and withdraw money
             'Inner Rank',  # Can deposit and withdraw money
             'Member']      # Can deposit money

    def __init__(self, name: str, color: str = "default", private=False):
        self.name = name
        self.color = color
        self.private = private
        self.bank_money: float = 0

        # Each member will be added there with there rank as the values : Format --> Key: Name -- Value: Rank {'name': 'rank'}
        self.members_rank = {}
        self.perms = {      # permission per rank in guild
            "Founder": '*',
            "Consultant": ['deposit', 'withdraw', 'kick', 'manage_house'],
            "High Rank": ['deposit', 'withdraw'],
            "Inner Rank": ['deposit', 'withdraw'],
            "Member": ['deposit']
        }
        self.base = None    # In developpement..


soloPlayer = guild("Solo-Player")

guild_list = [soloPlayer]
