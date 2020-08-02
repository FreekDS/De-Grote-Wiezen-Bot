from PIL import Image, ImageFont, ImageDraw
from typing import List, Tuple
from wiezenlibrary.Card import Card, CardType, Beilekes
from wiezenlibrary.Player import Player
from wiezenlibrary.Slag import Slag
import os

""" 
    CARDS NAMING SCHEME: cardType##.png 
    CARDS # VALUES: [1,13] 
    cardType VALUES: ["koeken", "harten", "klaveren", "schoppen"] 
"""

OUTPUT = "output"
INPUT = "assets"

COLOR1 = (255, 0, 0)
COLOR2 = (0, 0, 255)


class ImageGenerator:

    def __init__(self, deck=1):
        self.deck = deck

    @property
    def font(self):
        return ImageFont.truetype(f"{INPUT}/fonts/font.ttf", 60)

    def hand_to_image(self, player: Player, offset=10):
        if not player.hand:
            return
        images = list()
        for card in player.hand:
            images.append(Image.open(self._get_card_img(card)))
        widths, _ = zip(*(i.size for i in images))
        total_width = sum(widths) + (len(player.hand) - 1) * offset
        height = images[0].size[1]

        new_image = Image.new('RGB', (total_width, height + 4 * offset))
        draw = ImageDraw.Draw(new_image)

        x_offset = 0
        for index, image in enumerate(images):
            new_image.paste(image, (x_offset, 0))
            num = str(index + 1)
            tw, _ = draw.textsize(num)
            text_pos = (x_offset + widths[0] / 2 - tw, height + offset / 2)
            draw.text(text_pos, num, fill=(255,255,255), font=self.font)

            x_offset += image.size[0] + offset
            image.close()

        new_image.save(f'{OUTPUT}/hand.png')
        new_image.close()

    @staticmethod
    def remove_hand():
        os.remove(f'{OUTPUT}/hand.png')

    @staticmethod
    def remove_table():
        os.remove(f'{OUTPUT}/table.png')

    def _get_card_img(self, card: Card):
        return f"{INPUT}/decks/{self.deck}/{card.image_name}.png"

    def _get_card_size(self):
        with Image.open(self._get_card_img(Card(1, 1))) as image:
            return image.size

    def generate_table(self, table_layout: List[Tuple[Player or None, Card or None]], offset=20):
        images = list()
        names = list()
        for player, card in table_layout:
            images.append(Image.open(self._get_card_img(card)) if card else None)
            names.append(player.name if player else None)

        single_width, single_height = self._get_card_size()

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
            if image:
                new_image.paste(image, img_positions[index])
                image.close()

        draw = ImageDraw.Draw(new_image)

        text_positions = [
            (2 * offset + single_width, offset),
            (offset, single_height + 2 * offset),
            (2 * single_width + 3 * offset, single_height + 2 * offset),
            (2 * offset + single_width, 2 * single_height + 3 * offset)
        ]

        for index, name in enumerate(names):
            if name:
                fill = (255, 215, 0) if table_layout[index][0].is_dealer else (255, 255, 255)
                draw.text(text_positions[index], name, font=self.font, fill=fill)

        new_image.save(f"{OUTPUT}/table.png")
        new_image.close()

    @staticmethod
    def get_output(img_type: str):
        if img_type in ['table', 'hand']:
            return f"{OUTPUT}/{img_type}.png"
        else:
            return ""


if __name__ == '__main__':
    layout = [
        (Player("jefke", "0", False), Card(CardType.KLAVEREN, Beilekes.KONING)),
        (Player("louike", "1", False), Card(CardType.KOEKEN, 6)),
        (Player("franske", "2", False), Card(CardType.HARTEN, Beilekes.BOER)),
        (Player("mark", "3", True), None)
    ]

    p = Player("Charles", "4", True)
    p.give_card(Card(CardType.SCHOPPEN, 1))
    p.give_card(Card(CardType.KLAVEREN, 2))
    p.give_card(Card(CardType.KOEKEN, Beilekes.DAME))

    # ImageGenerator(1).generate_table(layout)
    ImageGenerator(1).hand_to_image(p)
