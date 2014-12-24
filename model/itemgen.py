"""
Contains code for random item generation.  Currently undeveloped and serves only strings.
"""

import random

__author__ = 'jessebostic'

class ItemGenerator:
    """Allows for random generation of items."""

    def __init__(self):
        """No state to be seen"""
        pass

    def generate_item(self):
        """Generate a new item.

        :return generated item
        """
        return self.Item()

    class Item:
        """Class for item instantiation"""

        placeholder_items = ["pair of silver boots", "hammer", "bag of marbles", "rock", "gold bar", "stick",
                             "platinumm hat", "pretty necklace", "pair of gloves", "broken iphone",
                             "scrap of rotten food", "soccer ball"]

        def __init__(self):
            """Makes random selection from a test list of strings.

            :return: random item
            """
            self.name = random.choice(self.placeholder_items)