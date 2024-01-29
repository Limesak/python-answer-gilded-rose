# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:

            item.sell_in -= 1

            # Exit logic if legendary item as the quality can't change
            if "Sulfuras" in item.name: 
                return
            
            # If the item is not an aged brie or a backstage pass, its quality decreases each day until it is 0
            # If it's a conjured item, double the decrease
            if "Aged Brie" not in item.name and "Backstage passes" not in item.name:
                if item.sell_in < 0 and "Conjured" not in item.name:
                    item.quality -= 2
                elif item.sell_in < 0 and "Conjured" in item.name:
                    item.quality -= 4
                elif "Conjured" not in item.name:
                    item.quality -= 1
                elif item.sell_in > 0 and "Conjured" in item.name:
                    item.quality -= 2
                item.quality = max(0, item.quality)

            # The quality of aged brie increases over time
            elif "Aged Brie" in item.name:
                item.quality += 1
                item.quality = min(item.quality, 50)

            # The quality of backstage passes increases over time more and more but drops to 0 after concert
            elif "Backstage passes" in item.name:
                if item.sell_in < 0:
                    item.quality = 0
                elif 10 >= item.sell_in >= 6:
                    item.quality += 2
                elif 5 >= item.sell_in >= 0:
                    item.quality += 3
                else:
                    item.quality += 1
                item.quality = min(50, item.quality)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
