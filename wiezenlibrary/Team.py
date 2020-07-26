class Team():
    def __init__(self,player_list: list):
        self.players=player_list
    def get_team_round_wins(self):
        count=0
        for player in self.players:
            count+=player.round_wins
        return count

    def has_player(self,player):
        return player in self.players

