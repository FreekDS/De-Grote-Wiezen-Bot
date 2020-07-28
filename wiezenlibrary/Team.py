import enum


class PLAYER_STRATS(enum.Enum):
    MISERIEAlONE = 0
    MISERIETEAM =1
    DANSENALONE = 2
    DANSENTEAM = 3
    TROELMETAZEN = 4
    TROELZONDERAZEN = 5
    SOLOSOLO = 6
    SOLOTEAM = 7
    SAAI=8#normaal spel met 2 teams van 2

    @staticmethod
    def get_oposite(strategy):
        if(strategy==PLAYER_STRATS.MISERIEAlONE):
            return PLAYER_STRATS.MISERIETEAM
        elif(strategy==PLAYER_STRATS.MISERIETEAM):
            return PLAYER_STRATS.MISERIEAlONE
        elif(strategy==PLAYER_STRATS.DANSENALONE):
            return PLAYER_STRATS.DANSENTEAM
        elif (strategy == PLAYER_STRATS.DANSENTEAM):
            return PLAYER_STRATS.DANSENALONE
        elif (strategy == PLAYER_STRATS.TROELMETAZEN):
            return PLAYER_STRATS.TROELZONDERAZEN
        elif (strategy == PLAYER_STRATS.TROELZONDERAZEN):
            return PLAYER_STRATS.TROELMETAZEN
        elif(strategy == PLAYER_STRATS.SOLOSOLO):
            return PLAYER_STRATS.SOLOTEAM
        elif (strategy == PLAYER_STRATS.SOLOTEAM):
            return PLAYER_STRATS.SOLOSOLO
        elif(strategy==PLAYER_STRATS.SAAI):
            return PLAYER_STRATS.SAAI


class Team():
    def __init__(self,player_list: list,Strategy:PLAYER_STRATS):
        self.players=player_list
        self.Strategy=Strategy
    def get_team_round_wins(self):
        count=0
        for player in self.players:
            count+=player.round_wins
        return count

    def has_player(self,player):
        return player in self.players

