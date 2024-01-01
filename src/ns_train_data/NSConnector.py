import os
import requests
import json
import datetime


class Station:

    def __init__(self, payload: dict):
        self.payload = payload

    def get_name(self, name_length: str = "lang") -> str:
        """Get station name."""
        return self.payload.get("namen").get(name_length)

    def get_uic_code(self) -> int:
        """Get station UIC code."""
        return self.payload.get("UICCode")


class NSConnector:

    def __init__(self, departure: str, arrival: str):
        self._credential = os.environ.get("REISINFORMATIE_API")
        self._headers = {"Ocp-Apim-Subscription-Key": self._credential}
        self.departure = self._add_station(departure)
        self.arrival = self._add_station(arrival)

    def _add_station(self, station: str) -> Station:
        """Get UIC code for particular station from NS API.

        :param station: full name of station to retrieve UIC code from.
        """
        api = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v2/stations?q={station}"
        station = self._get_api_response(api)
        payload = station.get("payload")

        # Station query should return only one result
        assert len(payload) == 1, "Station name is too ambiguous."

        return Station(payload[0])

    def _get_api_response(self, api: str) -> dict:
        """Get NS Api response."""
        response = requests.get(api, headers=self._headers)
        return json.loads(response.text)

    def get_uic_code(self, station: str):
        """Get UIC code of arrival/departure station."""
        assert station in {"arrival", "departure"}, "Station must be 'arrival' or 'departure'."
        station = self.__getattribute__(station)
        return station.get_uic_code()

    def get_journey(self):
        """Get Journey details."""
        print(datetime.datetime.now())

        api = f"https://gateway.apiportal.ns.nl/reisinformatie-api/api/v3/trips" \
              f"?originUicCode={self.get_uic_code('departure')}&destinationUicCode={self.get_uic_code('arrival')}" \
              f"&originWalk=false&originBike=false&originCar=false&destinationWalk=false&destinationBike=false" \
              f"&destinationCar=false&shorterChange=false&travelAssistance=false&searchForAccessibleTrip=false" \
              f"&localTrainsOnly=false&excludeHighSpeedTrains=false&excludeTrainsWithReservationRequired=false" \
              f"&product=GEEN&discount=NO_DISCOUNT&travelClass=2&passing=false&travelRequestType=DEFAULT"
        journey = self._get_api_response(api)

        return journey