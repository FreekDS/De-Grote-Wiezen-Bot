from PIL import Image
from typing import List
from Card import Card, CardType
from Player import Player
import os

""" CARDS NAMING SCHEME: cardType_#.png """
""" CARDS # VALUES: [1,13] """

OUTPUT = "output"
INPUT = "assets/decks/1"


class ImageGenerator:

    @staticmethod
    def hand_to_image(player: Player, offset=10):
        if not player.hand:
            return
        images = list()
        for card in player.hand:
            images.append(Image.open(f"{INPUT}/{CardType.get_name(card.type)}_{card.value}.png"))
        widths, _ = zip(*(i.size for i in images))
        total_width = sum(widths) + (len(player.hand) - 1) * offset
        height = images[0].size[1]

        new_image = Image.new('RGB', (total_width, height))
        x_offset = 0
        for image in images:
            new_image.paste(image, (x_offset, 0))
            x_offset += image.size[0] + offset

        new_image.save(f'{OUTPUT}/hand.png')

    @staticmethod
    def remove_hand():
        os.remove(f'{OUTPUT}/hand.png')

    @staticmethod
    def remove_table():
        os.remove(f'{OUTPUT}/table.png')

    @staticmethod
    def generate_table(self, table_cards: List[Card]):
        raise NotImplemented()
