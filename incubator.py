import items
from datetime import datetime, timedelta


class Incubator:
    def __init__(self):
        self.egg: items.Item = None
        self.active_egg = False
        self.timeEggReady: datetime = None


# Just some testing to understand DATETIME package
date1 = datetime.now()
date2 = date1 + timedelta(hours=36, minutes=40)
print(date1)
print(date2)
print(type(date2))
