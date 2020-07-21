from PIL import Image, ImageFont, ImageDraw
from typing import Dict
from wiezenlibrary.Card import Card, CardType
from wiezenlibrary.Player import Player
import os

""" CARDS NAMING SCHEME: cardType_#.png """
""" CARDS # VALUES: [1,13] """

OUTPUT = "output"
INPUT = "assets"


class ImageGenerator:

    @staticmethod
    def hand_to_image(player: Player, offset=10):
        if not player.hand:
            return
        images = list()
        for card in player.hand:
            images.append(Image.open(ImageGenerator._get_card_img(card)))
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
    def _get_card_img(card: Card):
        return "kaart.png"
        return f"{INPUT}/decks/1/{CardType.get_name(card.type)}_{card.value}.png"

    @staticmethod
    def generate_table(table_layout: Dict[Player, Card], offset=20):
        images = list()
        names = list()
        for player, card in table_layout.items():
            images.append(Image.open(ImageGenerator._get_card_img(card)))
            names.append(player.name)

        single_width, single_height = images[0].size

        width = 3 * single_width + 4 * offset
        height = 3 * single_height + 8 * offset

        new_image = Image.new('RGB', (width, height), (7, 99, 36))

        img_positions = [
            (single_width + 2 * offset, 3*offset),
            (offset, single_height + 4 * offset),
            (single_width * 2 + 3 * offset, single_height + 4 * offset),
            (single_width + 2 * offset, single_height * 2 + 5 * offset)
        ]

        for index, image in enumerate(images):
            new_image.paste(image, img_positions[index])

        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype(f"{INPUT}/fonts/font.ttf", 60)

        text_positions = [
            (2 * offset + single_width, offset),
            (offset, single_height + 2 * offset),
            (2 * single_width +  3 * offset, single_height + 2 * offset),
            (2 * offset + single_width, 2 * single_height + 3 * offset)
        ]

        for index, name in enumerate(names):
            draw.text(text_positions[index], name, font=font)

        new_image.save(f"{OUTPUT}/table.png")


if __name__ == '__main__':
    layout = {
        Player("", False, "jefke"): Card(1, 1),
        Player("", False, "louike"): Card(1, 1),
        Player("", False, "franske"): Card(1, 1),
        Player("", True, "mark"): Card(1, 1)
    }

    ImageGenerator.generate_table(layout)
