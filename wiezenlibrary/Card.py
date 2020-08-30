from enum import IntEnum


class Beilekes(IntEnum):
    BOER = 11
    DAME = 12
    KONING = 13

    @staticmethod
    def get_name(beileke: int):
        if beileke == int(Beilekes.BOER):
            return 'boer'
        elif beileke == int(Beilekes.DAME):
            return 'dame'
        elif beileke == int(Beilekes.KONING):
            return 'koning'


class CardType(IntEnum):
    SCHOPPEN = 0
    KLAVEREN = 1
    KOEKEN = 2
    HARTEN = 3

    @staticmethod
    def get_name(card_type: int):
        if int(card_type) == int(CardType.HARTEN):
            return 'harten'
        elif int(card_type) == int(CardType.SCHOPPEN):
            return 'schoppen'
        elif int(card_type) == int(CardType.KLAVEREN):
            return 'klaveren'
        else:
            return 'koeken'


class Card:
    def __init__(self, card_type: int, value: int):
        self.type: int = card_type
        self.value: int = value

    def __str__(self):
        second = self.value
        if self.value > 10:
            second = Beilekes.get_name(self.value)
        return f"{CardType.get_name(self.type)} {second}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if(other is None): return False
        return self.value == other.value and self.type == other.type

    def __lt__(self, other):
        selfVal = self.value if self.value is not 1 else 14
        otherval = other.value if other.value is not 1 else 14
        return selfVal < otherval

    def __gt__(self, other):
        selfVal = self.value if self.value is not 1 else 14
        otherval = other.value if other.value is not 1 else 14
        return selfVal > otherval

    @property
    def image_name(self):
        return f"{CardType.get_name(self.type)}{self.value:02d}"


if __name__ == '__main__':
    card1 = Card(CardType.KOEKEN, Beilekes.DAME)
    card2 = Card(CardType.KOEKEN, Beilekes.KONING)
    print(card1 < card2, card1.image_name)
    print(card1, card2, card2.image_name)
