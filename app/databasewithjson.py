import json
"""
Module for managing shipment data persistence.
This module handles loading and saving shipment data from/to a JSON file.
The shipments dictionary maps shipment IDs (strings) to shipment objects (dictionaries).
Type annotation expected:
    shipments: dict[str, dict] = {}
    - Key type: str (the shipment ID)
    - Value type: dict (the shipment object containing nested data like 'id' and other fields)
The shipments structure after loading will look like:
    {
        "shipment_id_1": {"id": "shipment_id_1", "field": "value", ...},
        "shipment_id_2": {"id": "shipment_id_2", "field": "value", ...},
    }
"""

shipments = {}

print("before load",shipments)

with open("shipments.json", "r") as json_file:
   data = json.load(json_file)

   for value in data:
         shipments[value['id']] = value

   print("after load",shipments)

def save():
     with open("shipments.json", "w") as json_file:
        json.dump(
            list(shipments.values()),
            json_file,
        )