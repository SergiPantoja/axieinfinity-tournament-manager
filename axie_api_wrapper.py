class Battle:
    """ 
    A Battle object represents a battle event between two axie players or between a player and AI that ocurred in the past.
    """
    def __init__(self, battle_id, player1_id, player2_id, winner, time_stamp, battle_type):
        self.__battle_id = int(battle_id)
        self.__player1_id = player1_id
        self.__player2_id = player2_id
        self.__winner = int(winner)
        self.__time_stamp = time_stamp
        self.__battle_type = battle_type
    
    def __str__(self):
        return f"Battle ID: {self.battle_id}, Battle Type: {self.battle_type}\n{self.player1_id} vs {self.player2_id}\n" \
                + f"Winner: {self.winner}\nDate: {self.date}, Time: {self.time}"

    @property
    def battle_id(self) -> int:
        return self.__battle_id
    
    @property
    def player1_id(self) -> str:
        # Returns the Eth address of the player
        return self.__player1_id

    @property
    def player2_id(self) -> str:
        # If pvp returns the Eth address of the second player.
        # If pve returns the ID of the PVE level
        return self.__player2_id
    
    @property
    def winner(self) -> str:
        return self.player1_id if self.winner == 0 else self.player2_id
    
    @property
    def date(self) -> str:
        return self.__time_stamp.split("T")[0]
    
    @property
    def time(self) -> str:
        return self.__time_stamp.split("T")[1]
    
    @property
    def battle_type(self) -> str:
        return self.__battle_type


def __create_battle(dict):
    # :param dict: Response from a battle request to the API
    battle_id = dict["id"]
    player1_id = dict["first_client_id"]
    player2_id = dict["second_client_id"]
    winner = dict["winner"]
    time_stamp = dict["created_at"]
    battle_type = dict["battle_type"]

    return Battle(battle_id, player1_id, player2_id, winner, time_stamp, battle_type)
