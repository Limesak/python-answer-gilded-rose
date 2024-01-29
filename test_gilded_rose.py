# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

class GildedRoseTest(unittest.TestCase):
    # This test checks if time is passing and the quality is changing for non legendary items 
    def test_1(self):
        items = [Item("foo", 10, 20)]
        current_quality = items[0].quality
        days_left = items[0].sell_in

        for i in range(days_left):
            gilded_rose = GildedRose(items)
            gilded_rose.update_quality()

            updated_quality = items[0].quality
            new_time_remaining = items[0].sell_in

            if updated_quality == current_quality and "Sulfuras" not in items[0].name:
                raise Exception("Non Sulfuras items need their qualities to change through time.")

            if new_time_remaining >= days_left:
                raise Exception("Time is not passing")

            current_quality = updated_quality
            days_left = new_time_remaining

    # This test checks that legendary items don't have decreasing value
    def test_2(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 0, 80)]
        original_quality = items[0].quality

        for i in range(items[0].sell_in):
            gilded_rose = GildedRose(items)
            gilded_rose.update_quality()

            if items[0].quality != original_quality:
                raise Exception("Quality can't change on legendary items")

    # ------------
    # This test checks if a non legendary item can start at a higher value than 50
    # def test_3(self):
    #     items = [Item("foo", 0, 100)]
    #     gilded_rose = GildedRose(items)
    #     gilded_rose.update_quality()
    #     if items[0].quality >= 50:
    #         print(items[0].quality)
    #         raise Exception("Quality of a non legendary item can't be above 50")
    #     print("test 3 OK")
    # This test is irrelevant: "Just for clarification, an item can never have its Quality increase above 50"
    # ------------

    # This test checks that an item cannot have a negative quality
    def test_4(self):
        items = [Item("foo", 20, 10)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            gilded_rose.update_quality()

            if items[0].quality < 0:
                raise Exception("Quality of an item cannot be negative")

    # This test checks if the old brie item has increasing quality over time instead of decreasing quality
    def test_5(self):
        items = [Item("Aged Brie", 3, 5)]
        current_quality = items[0].quality
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            gilded_rose.update_quality()

            if items[0].quality < current_quality:
                raise Exception("Aged Brie's quality must increase over time")
            else:
                current_quality = items[0].quality

    # This test checks if an item can have an increasing quality that goes above 50 when starting below 50
    def test_6(self):
        items = [Item("Aged Brie", 10, 45)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            gilded_rose.update_quality()

            if items[0].quality > 50:
                raise Exception("An item's quality can't go higher than 50")

    # This test checks if an item can have an increasing quality that goes above 50 when starting above 50
    def test_7(self):
        items = [Item("Aged Brie", 10, 55)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            gilded_rose.update_quality()

            if items[0].quality > 50:
                raise Exception("An item's quality can't go higher than 50")

    # This test checks if an item called "Backstage passes" has and increasing quality over time (before the concert)
    def test_8(self):
        items = [Item("Backstage passes", 15, 20)]
        current_quality = items[0].quality
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            gilded_rose.update_quality()

            if items[0].quality <= current_quality:
                raise Exception("Backstage passes can't have decreasing quality")
            else:
                current_quality = items[0].quality
    
    # This test checks if "Backstage passes"'s quality goes to 0 after the concert
    def test_9(self):
        items = [Item("Backstage passes", 5, 20)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in + 5):
            gilded_rose.update_quality()

            if items[0].sell_in < 0:
                assert items[0].quality == 0, "Backstage passes can only have a quality of 0 after the concert"
    
    # This test checks if "Backstage passes"'s quality increases by 2 when there's 10 days left
    def test_10(self):
        items = [Item("Backstage passes", 15, 10)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            previous_quality = items[0].quality
            gilded_rose.update_quality()
            if 10 >= items[0].sell_in >= 6 and items[0].quality != 50:
                assert 2 == (items[0].quality - previous_quality), "Between 10 and 6 days left, Backstage passes' quality must increase by 2 everyday"

    # This test checks if "Backstage passes"'s quality increases by 3 when there's 5 days left
    def test_11(self):
        items = [Item("Backstage passes", 15, 10)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            previous_quality = items[0].quality
            gilded_rose.update_quality()
            if 5 >= items[0].sell_in >= 0 and items[0].quality != 50:
                assert 3 == (items[0].quality - previous_quality), "Below 5 days left, Backstage passes' quality must increase by 3 everyday"
    
    # This test checks if "Conjured" items degrade twice as fast normal items when sell_in > 0
    def test_12(self):
        items = [Item("Conjured mana cake", 15, 35)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in):
            previous_quality = items[0].quality
            gilded_rose.update_quality()
            if items[0].sell_in > 0:
                assert (previous_quality - items[0].quality) == 2, "Conjured items must decrease twice as fast as normal ones"

    # This test checks if "Conjured" items degrade twice as fast normal items when sell_in < 0 
    def test_12(self):
        items = [Item("Conjured mana cake", 15, 35)]
        gilded_rose = GildedRose(items)

        for i in range(items[0].sell_in + 10):
            previous_quality = items[0].quality
            gilded_rose.update_quality()
            if items[0].sell_in < 0 and items[0].quality != 0:
                assert (previous_quality - items[0].quality) == 4, "Conjured items must decrease twice as fast as normal ones"


if __name__ == '__main__':
    unittest.main()
