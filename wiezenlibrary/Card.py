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
        if self.value == 11:
            second = 'boer'
        elif self.value == 12:
            second = 'dame'
        elif self.value == 13:
            second = 'koning'
        return f"{CardType.get_name(self.type)} {second}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.value == other.value and self.type == other.type

    def __lt__(self, other):
        return self.value < other.value and self.type == other.type

    def __gt__(self, other):
        return self.value < other.value and self.type == other.type


if __name__ == '__main__':
    card1 = Card(CardType.KOEKEN, 10)
    card2 = Card(CardType.KOEKEN, 2)
    print(card1 < card2)
    print(card1, card2)
