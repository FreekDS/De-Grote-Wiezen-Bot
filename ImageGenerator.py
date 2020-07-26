from PIL import Image, ImageFont, ImageDraw
from typing import Dict
from wiezenlibrary.Card import Card, CardType, Beilekes
from wiezenlibrary.Player import Player
import os

""" 
    CARDS NAMING SCHEME: cardType##.png 
    CARDS # VALUES: [1,13] 
    cardType VALUES: ["koeken", "harten", "klaveren", "schoppen"] 
"""

OUTPUT = "output"
INPUT = "assets"


class ImageGenerator:

    def __init__(self, deck=1):
        self.deck = deck

    def hand_to_image(self, player: Player, offset=10):
        if not player.hand:
            return
        images = list()
        for card in player.hand:
            images.append(Image.open(self._get_card_img(card)))
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

    def _get_card_img(self, card: Card):
        return f"{INPUT}/decks/{self.deck}/{card.image_name}.png"

    def generate_table(self, table_layout: Dict[Player, Card], offset=20):
        images = list()
        names = list()
        for player, card in table_layout.items():
            images.append(Image.open(self._get_card_img(card)))
            names.append(player.name)

        single_width, single_height = images[0].size

        width = 3 * single_width + 4 * offset
        height = 3 * single_height + 8 * offset

        new_image = Image.new('RGB', (width, height), (7, 99, 36))

        img_positions = [
            (single_width + 2 * offset, 3 * offset),
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
            (2 * single_width + 3 * offset, single_height + 2 * offset),
            (2 * offset + single_width, 2 * single_height + 3 * offset)
        ]

        for index, name in enumerate(names):
            fill = (255, 215, 0) if list(table_layout.keys())[index].is_dealer else (255, 255, 255)
            draw.text(text_positions[index], name, font=font, fill=fill)

        new_image.save(f"{OUTPUT}/table.png")


if __name__ == '__main__':
    layout = {
        Player("jefke", "0", False): Card(CardType.KLAVEREN, Beilekes.KONING),
        Player("louike", "1", False): Card(CardType.KOEKEN, 6),
        Player("franske", "2", False): Card(CardType.HARTEN, Beilekes.BOER),
        Player("mark", "3", True): Card(CardType.KOEKEN, Beilekes.DAME)
    }

    ImageGenerator(1).generate_table(layout)
