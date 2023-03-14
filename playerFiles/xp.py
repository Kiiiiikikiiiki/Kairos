import embeds


# exp CONSTANT
LVL = "lvl"
CURRENT_EXP = "current_exp"
NEXT_LVL_EXP = "next_lvl_exp"  
MAX_LVL = "max_level"                                        


class exp:

    # Accescible constant
    PLAYER_XP_TYPE = "player" 
    MINER_XP_TYPE = "mining"
    FISHING_XP_TYPE = "fishing"
    COOKING_XP_TYPE = "cooking"
    HUNTER_XP_TYPE = "hunting"
    SMITHING_XP_TYPE = "smithing"
    FARMER_XP_TYPE = "farming"
    BUTCHER_XP_TYPE = "butching"

    SKILLS_EMOJI = {
        PLAYER_XP_TYPE: "🙋🏻‍♂️",
        MINER_XP_TYPE: "⛏️"
    }

    __EXP_PER_LEVEL = [100, 200, 300, 400, 600, 800, 1000,
         1500, 2000, 2500, 3500, 4500, 5500, 7500, 9500, 11500]     # How much exp does it require a player to go to next level for each level

    def __init__(self):

        # All skills xp
        self.skills = {
            f"{self.PLAYER_XP_TYPE}": {
                f"{LVL}": 0,
                f"{CURRENT_EXP}": 0,
                f"{NEXT_LVL_EXP}": self.__EXP_PER_LEVEL[0],
                f"{MAX_LVL}": 15
            },
            # MINER SKILLS
            f"{self.MINER_XP_TYPE}": {
                f"{LVL}": 0,
                f"{CURRENT_EXP}": 0,
                f"{NEXT_LVL_EXP}": self.__EXP_PER_LEVEL[0],
                f"{MAX_LVL}": 60
            },
            # FINSHING SKILL
            f"{self.FISHING_XP_TYPE}": {
                f"{LVL}": 0,
                f"{CURRENT_EXP}": 0,
                f"{NEXT_LVL_EXP}": self.__EXP_PER_LEVEL[0],
                f"{MAX_LVL}": 60
            }
        }

        # FISHING SKILL 

        # COOKING SKILL

        # HUNTER SKILL

        # SMITHING SKILL 

        # FARMER SKILL

        # BUTCHER SKILL
    
    # Add experience to a selected skills
    def addXp(self, xp_type: str, amountXp: float, player_name: str):
        skill = self.skills.get(xp_type)    # get the dict for the selected skill

        # Check if the player has enough experience to level up & add the experience to the pre-selected skill
        if skill.get(LVL) != skill.get(MAX_LVL):
            skill[CURRENT_EXP] += amountXp     # Add the experience to the skill
            # Make a save of the skill modification
            self._save_skill(xp_type=xp_type, skill=skill)
            # Do the player level up ?
            if skill.get(CURRENT_EXP) >= skill.get(NEXT_LVL_EXP):
                skill[CURRENT_EXP] = skill.get(CURRENT_EXP) - skill.get(NEXT_LVL_EXP) # the over xp will be added to the player
                skill[LVL] += 1     # level up
                skill[NEXT_LVL_EXP] = self.__EXP_PER_LEVEL[skill.get(LVL)]
                # Make a save of the skill modifications
                self._save_skill(xp_type=xp_type, skill=skill)

                # Since player level up, we return and embed that can be used to show that the player has level up.
                return True, embeds.levelUp_embed(player_name=player_name, skill_name=xp_type, skill_emoji=self.SKILLS_EMOJI.get(xp_type), new_lvl=self.skills.get(xp_type).get(LVL))
            else:
                return False, None
        else:
            return False, None

    def _save_skill(self, xp_type: str, skill: dict):
        '''
        save the modification done to a skill
        '''
        self.skills[xp_type] = skill
    