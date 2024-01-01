import os
import requests
import json


class NSConnector:

    def __init__(self):
        self._credential = os.environ.get("REISINFORMATIE_API")
        self._headers = {"Ocp-Apim-Subscription-Key": self._credential}
        self.stations = []

    def _retrieve_stations(self, station: str) -> None:
        """Get UIC code for particular station from NS API.

        :param station: full name of station to retrieve UIC code from.
        """
        api = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations?q={station}"
        response = requests.get(api, headers=self._headers)

        station = json.loads(response.text)
        payload = station.get("payload")

        # Station query should return only one result
        assert len(payload) == 1, "Station name is too ambiguous."

        self.stations.append(Station(payload))

    def get_uic_codes(self) -> dict[str: int]:
        """Returns UIC codes for each registered station

        :return: Dictionary with name and according UIC codes.
        """
        uic_dict = {station.get_name(): station.get_uic_code() for station in self.stations}


class Station:

    def __init__(self, payload: dict):
        self.payload = payload

    def get_name(self, name_length: str = "lang") -> str:
        """Get station name."""
        return self.payload.get("namen").get(name_length)

    def get_uic_code(self) -> int:
        """Get station UIC code."""
        return self.payload.get("UICCode")