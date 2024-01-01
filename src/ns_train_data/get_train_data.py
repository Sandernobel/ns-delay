import datetime

from NSConnector import NSConnector

connector = NSConnector(departure="Amsterdam Amstel", arrival="Utrecht Centraal")
print(connector.get_journey())