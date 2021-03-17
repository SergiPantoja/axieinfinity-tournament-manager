import requests
from requests.exceptions import HTTPError


class Battle:
    """ 
    A Battle object represents a battle event between two axie players or between a player and AI that ocurred in the past.
    """
    def __init__(self, battle_id, player1_id, player2_id, winner, time_stamp, battle_type):
        self.__battle_id = battle_id
        self.__player1_id = player1_id
        self.__player2_id = player2_id
        self.__winner = int(winner)
        self.__time_stamp = time_stamp
        self.__battle_type = battle_type
    
    def __str__(self):
        return f"Battle ID: {self.battle_id}, Battle Type: {self.battle_type}\n{self.player1_id} vs {self.player2_id}\n" \
                + f"Winner: {self.winner}\nDate: {self.date}, Time: {self.time}"

    @property
    def battle_id(self) -> str:
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
        return self.player1_id if self.__winner == 0 else self.player2_id
    
    @property
    def date(self) -> str:
        return self.__time_stamp.split("T")[0]
    
    @property
    def time(self) -> str:
        return self.__time_stamp.split("T")[1]
    
    @property
    def battle_type(self) -> str:
        return self.__battle_type


def _create_battle(dict):
    # :param dict: Response from a battle request to the API
    battle_id = dict["id"]
    player1_id = dict["first_client_id"]
    player2_id = dict["second_client_id"]
    winner = dict["winner"]
    time_stamp = dict["created_at"]
    battle_type = dict["battle_type"]

    return Battle(battle_id, player1_id, player2_id, winner, time_stamp, battle_type)


class ApiClient:
    """
    Main class to interact with the Axie Infinity API
    """
    def __init__(self, url="https://lunacia.skymavis.com/game-api/"):
        self.url = url
    
    def _make_request(self, endpoint: str):
        """
        Handles status codes and returns a python dictionary with the response data
        """
        url = self.url + endpoint
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            if r:
                # Successfull but different status_code
                raise Exception(f"Request to {url} unsuccessful. Status Code: {r.status_code}")
            else:
                r.raise_for_status()
            
    def get_latest_battles(self, limit=10, offset=0):
        """
        Returns a list (actually a generator) of Battle with the latest battles in Axie Infinity.
        :param limit: Amount of battles to request.
        :param offset: Number of battles to remove from the result starting from the most recent to the oldest.
        """
        
        url = f"battles?limit={str(limit)}&offset={str(offset)}"
        battles = self._make_request(url)["items"]
        return (_create_battle(b) for b in battles)
    
    def get_battle_by_id(self, battle_id: str):
        """
        Returns a Battle object. The battle of id <battle_id>.
        """

        battle = self._make_request(f"battles/{str(battle_id)}")
        return _create_battle(battle)

    def get_user_battles(self, eth_addr: str, limit=10, offset=0):
        """
        Returns a generator of the latest 10 battles of the user with the Ethereum account <eth_addr>.
        :param eth_addr: Ethereum address of the player.
        :param limit: Amount of battles to request.
        :param offset: Number of battles to remove from the result starting from the most recent to the oldest.
        """
        url = f"clients/{eth_addr}/battles?limit={limit}&offset={offset}"
        battles = self._make_request(url)["items"]
        return (_create_battle(b) for b in battles)


if __name__ == "__main__":
    a = ApiClient()
    battles = a.get_latest_battles(100, 3)
    for i in battles:
        print(i, '\n')
    
    print("\n\n")

    battle2 = a.get_battle_by_id("3424")
    print(battle2, "\n")

    print("\n\n")

    #player_battles = a.get_user_battles('<eth_addr>', limit=100, offset=20)
    #for i in player_battles:
    #    print(i, "\n")
