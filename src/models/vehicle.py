from enum import Enum 

class VehicleType(Enum):
    MINI= "MINI"
    BUS = "BUS"

class Vehicle:
    def __init__(self, vehicle_type: VehicleType, plate_number: str):
        self.type = vehicle_type
        self.plate_number = plate_number