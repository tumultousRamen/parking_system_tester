from typing import List, Optional 
from .models.vehicle import Vehicle, VehicleType
from .models.parking_spot import ParkingSpot

class ParkingStation:
    def __init__(self, mini_spots: int, bus_spots: int):
        self.spots = (
            [ParkingSpot(f"MINI_{i}", VehicleType.MINI) for i in range(mini_spots)] +
            [ParkingSpot(f"BUS_{i}", VehicleType.BUS) for i in range(bus_spots)]
        )

    def park_vehicle(self, vehicle: Vehicle) -> Optional[str]:
        """"
        This function attempts to park a vehicle

        Args:
        vehicle: Vehicle 

        Returns:
        spot_id : Optional[str] Spot ID if attempt successful, None if not
        """

        for spot in self.spots:
            if not spot.is_occupied and spot.type == vehicle.type:
                spot.is_occupied = True 
                spot.vehicle = vehicle
                return spot.id
            
        return None
    
    def get_available_spots(self, vehicle_type: VehicleType) -> List[str]:
        """
        This function finds all available spot IDs in the Parking Station 
        for a particular VehicleType

        Args:
        vehicle: VehicleType

        Returns:
        List[str]: List of available spots IDs for a particular VehicleType
        """

        return [
            spot.id for spot in self.spots
            if spot.type == vehicle_type and not spot.is_occupied
        ]
    
    