from .vehicle import VehicleType

class ParkingSpot:
    def __init__(self, spot_id: str, spot_type: VehicleType):
        self.id = spot_id
        self.type = spot_type
        self.is_occupied = False 
        self.vehicle = None 
        
