import AbstractStrategy


class Team:
    def __init__(self, player_list: list, Strategy: AbstractStrategy):
        self.players = player_list
        self.Strategy = Strategy

    def get_team_round_wins(self):
        count = 0
        for player in self.players:
            count += player.round_wins
        return count

    def check_team_win(self, other_team):
        teamwins = self.get_team_round_wins()
        enemywins = other_team.get_team_round_wins()
        return self.Strategy.check_win(teamwins, enemywins)

    def give_points(self):
        for player in self.players:
            # The 0 given here could be the amount of won "slagen"
            # This is for a possible fututre expansion where the amount of won slagen changes the amount of point you get
            player.total_points += self.Strategy.get_scores(0)

    def has_player(self, player):
        return player in self.players

    def __str__(self):
        if len(self.players) == 1:
            return self.players[0].name
        if len(self.players) == 2:
            return self.players[0].name + " en " + self.players[1].name
        if len(self.players) == 3:
            return self.players[0].name + " , " + self.players[1].name + " en " + self.players[2].name
