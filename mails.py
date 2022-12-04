import items


class Mails:
    def __init__(self, message: str, sender: str, gifts: list[items.Item] = None, quest=None):
        self.message = message
        self.sender = sender
        self.gifts = gifts
        self.quest = quest
