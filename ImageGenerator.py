from PIL import Image, ImageFont, ImageDraw
from typing import List, Tuple
from wiezenlibrary.Card import Card, CardType, Beilekes
from wiezenlibrary.Player import Player
from wiezenlibrary.Team import Team, PLAYER_STRATS
from wiezenlibrary.Slag import Slag
import os

""" 
    CARDS NAMING SCHEME: cardType##.png 
    CARDS # VALUES: [1,13] 
    cardType VALUES: ["koeken", "harten", "klaveren", "schoppen"] 
"""

OUTPUT = "output"
INPUT = "assets"

COLOR1 = (255, 255, 255)
COLOR2 = (0, 0, 0)
BOARD_GREEN = (7, 99, 36)
BOARD_GREY = (92, 90, 80)


class ImageGenerator:

    def __init__(self, deck=1):
        self.deck = deck

    @property
    def font(self):
        return ImageFont.truetype(f"{INPUT}/fonts/font.ttf", 60)

    @property
    def small_font(self):
        return ImageFont.truetype(f"{INPUT}/fonts/font.ttf", 40)

    @staticmethod
    def slag_to_layout(current_slag: Slag, players):
        if not current_slag:
            raise AttributeError("Slag cannot be None")
        new_layout: List[Tuple[Player, Card or None]] = list()
        not_played: List[Player] = list()
        for player in players:
            for obj in current_slag.card_player_tuple:
                if player == obj[0]:
                    new_layout.append(obj)
                    break
            else:
                not_played.append(player)
        for player in not_played:
            new_layout.append((player, None))
        return new_layout

    def game_score(self, slag_amounts: List[int], teams: List[Team]):
        width = 400
        height = 80

        team1 = [t.name for t in teams[0].players]
        team2 = [t.name for t in teams[1].players]

        new_image = Image.new('RGB', (width, height), BOARD_GREY)
        draw = ImageDraw.Draw(new_image)
        score1_w, th = draw.textsize(str(slag_amounts[1]), font=self.font)
        vs_w, _ = draw.textsize('-')
        score2_w, _ = draw.textsize(str(slag_amounts[1]), font=self.font)

        total_w = score1_w + 4 * vs_w + score2_w

        start_x = (width - total_w * 1.2) / 2
        center_h = (height - th) / 2

        score_positions = [
            (start_x, center_h),
            (start_x + score1_w, center_h),
            (start_x + score1_w + 4 * vs_w, center_h)
        ]

        draw.text(score_positions[0], str(slag_amounts[0]), fill=COLOR1, font=self.font)
        draw.text(score_positions[1], ' - ', fill=(255, 255, 255), font=self.font)
        draw.text(score_positions[2], str(slag_amounts[1]), fill=COLOR2, font=self.font)

        y_offset = 0
        for name in team1:
            draw.text((10, y_offset), name, fill=COLOR1, font=self.small_font)
            y_offset += th

        y_offset = 0
        for name in team2:
            nw, _ = draw.textsize(name, font=self.small_font)
            draw.text((width - nw - 4, y_offset), name, fill=COLOR2, font=self.small_font)
            y_offset += th

        new_image.save(f"{OUTPUT}/score.png")
        return new_image

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
            draw.text(text_pos, num, fill=(255, 255, 255), font=self.font)

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

    @staticmethod
    def remove_score():
        os.remove(f'{OUTPUT}/score.png')

    def _get_card_img(self, card: Card):
        return f"{INPUT}/decks/{self.deck}/{card.image_name}.png"

    def _get_card_size(self):
        with Image.open(self._get_card_img(Card(1, 1))) as image:
            return image.size

    def _get_card_type_img(self, card_type: CardType):
        return f"{INPUT}/decks/{self.deck}/{CardType.get_name(card_type)}_icon.png"

    def _table_base(self, current_slag: Slag, players: List[Player], teams: List[Team], offset=20):
        images = list()
        names = list()
        table_layout = self.slag_to_layout(current_slag, players)
        for player, card in table_layout:
            images.append(Image.open(self._get_card_img(card)) if card else None)
            names.append(player.name if player else None)

        single_width, single_height = self._get_card_size()

        width = 3 * single_width + 4 * offset + 40
        height = 3 * single_height + 8 * offset

        new_image = Image.new('RGB', (width, height), BOARD_GREEN)

        img_positions = [
            (single_width + 2 * offset, 3 * offset),
            (offset, single_height + 4 * offset),
            (single_width * 2 + 3 * offset, single_height + 4 * offset),
            (single_width + 2 * offset, single_height * 2 + 5 * offset)
        ]

        if current_slag.troef:
            troef_image = Image.open(self._get_card_type_img(current_slag.troef))
            size = int(single_width / 2)
            scaling = int(size / troef_image.size[0])
            troef_image.resize((troef_image.size[0] * scaling, troef_image.size[1] * scaling))
            position = (
                int(width / 2 - troef_image.size[0] / 1.5),
                int((height - troef_image.size[1]) / 2)
            )
            new_image.paste(troef_image, position, troef_image)

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
                fill = COLOR1 if teams[0].has_player(table_layout[index][0]) else COLOR2
                draw.text(text_positions[index], name, font=self.font, fill=fill)

        new_image.save(f"{OUTPUT}/tableBase.png")
        return new_image

    def generate_table(self, current_slag: Slag, players: List[Player], teams: List[Team], offset=20):
        table_base = self._table_base(current_slag, players, teams, offset)
        scores = self.game_score([0, 0], teams)

        full_height = table_base.size[1] + scores.size[1]
        new_image = Image.new('RGBA', (table_base.size[0], full_height))

        center_x = int((table_base.size[0] - scores.size[0]) / 2)
        new_image.paste(scores, (center_x, 0))
        new_image.paste(table_base, (0, scores.size[1]))
        new_image.save(f"{OUTPUT}/table.png")
        new_image.close()
        table_base.close()
        scores.close()

    @staticmethod
    def get_output(img_type: str):
        if img_type in ['table', 'hand']:
            return f"{OUTPUT}/{img_type}.png"
        else:
            return ""


if __name__ == '__main__':
    gen = ImageGenerator(1)

    players = [
        Player("Jefke", "0", False),
        Player("Louike", "1", False),
        Player("Franske", "2", False),
        Player("Mark", "3", True)
    ]

    slag = Slag(CardType.KOEKEN)
    slag.lay_card(players[0], Card(CardType.KLAVEREN, 10))
    slag.lay_card(players[1], Card(CardType.HARTEN, 5))

    team1 = Team([players[0]], PLAYER_STRATS.SAAI)
    team2 = Team([players[1], players[2], players[3]], PLAYER_STRATS.SAAI)

    gen.generate_table(slag, players, [team1, team2])

    p = Player("Charles", "4", True)
    p.give_card(Card(CardType.SCHOPPEN, 1))
    p.give_card(Card(CardType.KLAVEREN, 2))
    p.give_card(Card(CardType.KOEKEN, Beilekes.DAME))

    gen.hand_to_image(p)

    gen.generate_table(slag, players, teams=[team1, team2])
    gen.game_score([1, 1], [team1, team2])
