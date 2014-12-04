import random

__author__ = 'jessebostic'

class ItemGenerator:

    def __init__(self):
        pass

    def generate_item(self):
        return self.Item()

    class Item:
        placeholder_items = ["pair of silver boots", "hammer", "bag of marbles", "rock", "gold bar", "stick", "platinumm hat",
                             "pretty necklace", "pair of gloves", "broken iphone", "scrap of rotten food", "soccer ball"]
        def __init__(self):
            self.name = random.choice(self.placeholder_items)